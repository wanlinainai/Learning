# NFTurbo

## 记录问题

### 统一状态机

一个状态机包含了几个要素：

1. 状态（state）：代表系统可能处于的各种状态，比如：“已下单”、“已支付”、“已发货”、“取消”等
2. 事件（event）：触发状态转换的事件，比如：“下单”、“支付”、“发货”等
3. 转换（transitions）：定义状态之间的转换规则，也就是在某一个事件发生的时候，系统从一个状态转换到另一个状态的规则
4. 动作（Actions）：在状态转换发生的时候执行的操作或行为。

代码实现（简易实现）：

**interface  StateMachine**

```java
public interface StateMachine<STATE, EVENT> {

    /**
     * 状态机转移
     *
     * @param state
     * @param event
     * @return
     */
    public STATE transition(STATE state, EVENT event);
}
```

**BaseStateMachine**

```java
public class BaseStateMachine<STATE, EVENT> implements StateMachine<STATE, EVENT> {
    private Map<String, STATE> stateTransitions = Maps.newHashMap();

    protected void putTransition(STATE origin, EVENT event, STATE target) {
        stateTransitions.put(Joiner.on("_").join(origin, event), target);
    }

    @Override
    public STATE transition(STATE state, EVENT event) {
        STATE target = stateTransitions.get(Joiner.on("_").join(state, event));
        if (target == null) {
            throw new BizException("state = " + state + " , event = " + event, STATE_MACHINE_TRANSITION_FAILED);
        }
        return target;
    }
}
```

**OrderStateMachine**

```java
public class OrderStateMachine extends BaseStateMachine<TradeOrderState, TradeOrderEvent> {

    public static final OrderStateMachine INSTANCE = new OrderStateMachine();

    {
        putTransition(TradeOrderState.CREATE, TradeOrderEvent.CONFIRM, TradeOrderState.CONFIRM);
        putTransition(TradeOrderState.CONFIRM, TradeOrderEvent.PAY, TradeOrderState.PAID);
        //库存预扣减成功，但是未真正扣减成功，也能支付/取消，不能因为延迟导致用户无法支付/取消。
        putTransition(TradeOrderState.CREATE, TradeOrderEvent.PAY, TradeOrderState.PAID);
        putTransition(TradeOrderState.CREATE, TradeOrderEvent.CANCEL, TradeOrderState.CLOSED);
        putTransition(TradeOrderState.CREATE, TradeOrderEvent.TIME_OUT, TradeOrderState.CLOSED);

        //订单创建过程中失败，推进到废弃态，这种状态用户看不到订单
        putTransition(TradeOrderState.CREATE, TradeOrderEvent.DISCARD, TradeOrderState.DISCARD);
        putTransition(TradeOrderState.CONFIRM, TradeOrderEvent.DISCARD, TradeOrderState.DISCARD);

        //已支付后，再确认，状态不变
        putTransition(TradeOrderState.PAID, TradeOrderEvent.CONFIRM, TradeOrderState.PAID);

        putTransition(TradeOrderState.CONFIRM, TradeOrderEvent.CANCEL, TradeOrderState.CLOSED);
        putTransition(TradeOrderState.CONFIRM, TradeOrderEvent.TIME_OUT, TradeOrderState.CLOSED);

        putTransition(TradeOrderState.PAID, TradeOrderEvent.FINISH, TradeOrderState.FINISH);
    }
}
```

拿着订单状态机举例：

订单的不同状态都是有着详细的执行逻辑的，状态机就是将状态的流转的过程封装在一起，可以执行`已下单` ----> `支付`事件。

我们做的设计的状态机是用的HashMap来进行存储具体的状态，`初始状态 + 事件`作为key，`目标状态`是value。在使用的时候只需要在类加载的时候将提前设计的状态流转部分存入到Key中，之后在进行订单状态流转的时候会判断这个Map中是否存在真正的Key值，存在就可以进行操作，进行写库操作。没有这个状态流转的话会自动失败，拒绝写库，抛出错误。

```java
public TradeOrder confirm(OrderConfirmRequest request) {
        this.setOrderConfirmedTime(request.getOperateTime());
        TradeOrderState orderState = OrderStateMachine.INSTANCE.transition(this.getOrderState(), request.getOrderEvent());
        this.setOrderState(orderState);
        return this;
    }
```

### 自定义Starter

步骤：

1. 添加Starter依赖
2. 实现Starter自动配置

​	如果starter需要配置属性，可以通过一个配置属性类来实现，使用`@ConfigurationProperties`注解。

```java
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = XxlJobProperties.PREFIX)
public class XxlJobProperties {

    public static final String PREFIX = "spring.xxl.job";

    private boolean enabled;

    private String adminAddresses;

    private String accessToken;

    private String appName;

    private String ip;

    private int port;

    private String logPath;

    private int logRetentionDays = 30;

    public boolean isEnabled() {
        return enabled;
    }
	...
}
```

3. 定义configuration，在其中创建需要的Bean。

```java
@Configuration
@EnableConfigurationProperties(XxlJobProperties.class)
public class XxlJobConfiguration {

    private static final Logger logger = LoggerFactory.getLogger(XxlJobConfiguration.class);

    @Autowired
    private XxlJobProperties properties;

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = XxlJobProperties.PREFIX, value = "enabled", havingValue = "true", matchIfMissing = true)
    public XxlJobSpringExecutor xxlJobExecutor() {
        logger.info(">>>>>>>>>>> xxl-job config init.");
        XxlJobSpringExecutor xxlJobSpringExecutor = new XxlJobSpringExecutor();
        xxlJobSpringExecutor.setAdminAddresses(properties.getAdminAddresses());
        xxlJobSpringExecutor.setAppname(properties.getAppName());
        xxlJobSpringExecutor.setIp(properties.getIp());
        xxlJobSpringExecutor.setPort(properties.getPort());
        xxlJobSpringExecutor.setAccessToken(properties.getAccessToken());
        xxlJobSpringExecutor.setLogPath(properties.getLogPath());
        xxlJobSpringExecutor.setLogRetentionDays(properties.getLogRetentionDays());
        return xxlJobSpringExecutor;
    }
}
```

> `@Bean`注解声明了一个bean，并且使用`@ConditionOnMissingBean`指定这个Bean的创建条件，在缺失的时候创建。

> `@ConditionOnProperty(prefix = XxlJobProperties.PERFIX, value = "enabled", havingValue = "true")`约定了我们配置`spring.xxl.job.enabled=true`的时候才会生效。

4. 创建配置类入口文件

Spring3.0之后需要创建：`org.springframework.boot.autoconfigure.AutoConfiguration.imports`。

文件内写上具体的Configuration即可。

