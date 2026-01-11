# 芋道

## 模块分布

| 业务系统                                                     | 通用模块              | 框架组件            |
| ------------------------------------------------------------ | --------------------- | ------------------- |
| 商城Mall                                                     | System系统功能        | Web技术组件         |
| OA自动化办公                                                 | Infra基础设施         | Security安全组件    |
| ERP企业资源计划系统（ERP 就是一套把企业里“人、财、物、产、供、销”等所有核心业务统一管理起来的软件系统） | BPM工作流程           | MyBatis数据库组件   |
| CRM客户关系管理系统（CRM 是专门用来“管客户、促成交、提复购”的系统） | Pay支付系统           | Redis缓存组件       |
| CMS内容管理系统（解决的是内容多、更新频繁、非技术人员也可以修改内容的系统，例如公司官网、新闻，产品介绍等） | Member会员中心        | MQ中间件            |
| BBS论坛社区系统（社区系统，贴吧一类）                        | Visualization数据报表 | JOB定时任务         |
|                                                              |                       | Protection组件      |
|                                                              |                       | Monitor监视器组件   |
|                                                              |                       | Test测试            |
|                                                              |                       | Flowable工作流      |
|                                                              |                       | Data Permission组件 |
|                                                              |                       | Tenant 业务组件     |
|                                                              |                       | Pay业务组件         |
|                                                              |                       | SMS业务组件         |
|                                                              |                       | Social 业务组件     |
|                                                              |                       | Operate Log业务组件 |



## 功能权限

### 如何设计一个权限系统

- 目标
- 权限模型
- 选择方案

#### 目标：最基础的解决问题就是校验用户是否可以进行某一个操作

1. 灵活配置权限
2. 多种级别的权限（菜单、按钮、URL）



#### 权限模型

1. RBAC

   全称：基于角色的访问控制

   概念：简而言之，总共有三个类型（用户、角色、权限），用户和权限是通过角色进行交集绑定的，也就是某一个用户有那一些角色，这些角色有哪一些权限。只要用户和角色、角色和权限之间存在交集，就是该用户具有某一个权限。

   好处：简单可复用。

2. ABAC

   全称：基于属性的访问控制

   概念：权限是否被允许，是由以下四个信息共同决定的。

   1. 对象：对象是当前请求访问资源的用户。例如：用户的属性包括ID、个人资源、角色、部门和组织成员身份标识
   2. 资源：资源是当前用户要访问的资产和对象。例如文件、数据、服务器甚至是API
   3. 操作：用户试图对资源进行的操作。常见的操作包括：读取、写入、编辑、删除等
   4. 环境信息：环境是每一个访问请求的上下文。比如：访问的时间和位置，对象的设备、通信协议等

   举例说明：

   以阿里为例。P5（职级）的研发（职位）同学，在公司内网（环境）下，可以查看和下载（操作）代码（资源）。

   部门经理（部门），可以查看、编辑（操作）自己部门下的所有订单（资源）。

   好处：实现非常灵活的权限控制，几乎满足所有类型需求。

   使用场景：用户量很多，授权复杂的场景。

   表结构：![image-20260104005519584](images/yudao/image-20260104005519584.png)





## 用户认证

系统提供了两种类型的用户，分别满足对应的管理后台、用户App 场景。

![image-20260104222401945](images/yudao/image-20260104222401945.png)

两种不同类型的用户分别对应两个表：**system_users**、**member_user**表。

> 为什么不使用统一的用户表？
>
> 新增一个type字段表示用户类型，主要是一开始考虑到两个模块是不同的组进行开发，尽量不互相污染数据，采取了多个用户表的方案。

如果之间需要进行关联，可以通过中间表进行处理。**system_oauth2_access_token**。字段：user_type。



### 设计一个双Token系统

双Token机制出现的需求是：

1. Token过期时间不会设计的很长，所以很可能经常需要用户重新登录，影响用户体验。
2. 设置长期的Token安全性降低。

表设计：**访问令牌**和**刷新令牌**

![image-20260105223600025](images/yudao/image-20260105223600025.png)

一个是用来存储访问令牌的，另一个是用来存储刷新Token的。

整体步骤：登录接口中有创建Token的方法，在这个方法中需要添加一个方法插入登录日志入库。之后创建访问令牌。创建刷新令牌和访问令牌入库。创建刷新令牌的时候不需要设置到Redis中，原因是这个刷新令牌的过期时间很长30天。之后设置访问令牌，先将访问令牌设置到数据库中，之后设置到Redis中。

如果用户注销登录，删除访问令牌（删除数据库中的和Redis中的），之后删除刷新令牌。之后所有接口进行校验的时候就会出现用户认证失败的问题自动重定向到登录页面。

### 开发测试的时候设置认证Token

在Token过滤器中加上Mock掉数据的操作。设计的要求是：

1. Token开头必须是：test
2. test之后跟一个数字，表示用户编号
3. 需要动态配置Mock开启状态：

```yaml
yudao:
  security:
    mock-enable: true
```

### 实现URL是否需要登录

主要是利用Spring Security中的permitAll()方法。

1. 首先有一些静态资源需要设置成permitAll。之后获取全部接口，观察这些接口中的是否包含@PermitAll。按照请求方式作为Map分别进行处理。

```java
  private Multimap<HttpMethod, String> getPermitAllUrlsFromAnnotations() {
        Multimap<HttpMethod, String> result = HashMultimap.create();
        // 获得接口对应的 HandlerMethod 集合
        RequestMappingHandlerMapping requestMappingHandlerMapping = (RequestMappingHandlerMapping)
                applicationContext.getBean("requestMappingHandlerMapping");
        Map<RequestMappingInfo, HandlerMethod> handlerMethodMap = requestMappingHandlerMapping.getHandlerMethods();
        // 获得有 @PermitAll 注解的接口
        for (Map.Entry<RequestMappingInfo, HandlerMethod> entry : handlerMethodMap.entrySet()) {
            HandlerMethod handlerMethod = entry.getValue();
            if (!handlerMethod.hasMethodAnnotation(PermitAll.class) // 方法级
                    && !handlerMethod.getBeanType().isAnnotationPresent(PermitAll.class)) { // 接口级
                continue;
            }
            Set<String> urls = new HashSet<>();
            if (entry.getKey().getPatternsCondition() != null) {
                urls.addAll(entry.getKey().getPatternsCondition().getPatterns());
            }
            if (entry.getKey().getPathPatternsCondition() != null) {
                urls.addAll(convertList(entry.getKey().getPathPatternsCondition().getPatterns(), PathPattern::getPatternString));
            }
            if (urls.isEmpty()) {
                continue;
            }

            // 特殊：使用 @RequestMapping 注解，并且未写 method 属性，此时认为都需要免登录
            Set<RequestMethod> methods = entry.getKey().getMethodsCondition().getMethods();
            if (CollUtil.isEmpty(methods)) {
                result.putAll(HttpMethod.GET, urls);
                result.putAll(HttpMethod.POST, urls);
                result.putAll(HttpMethod.PUT, urls);
                result.putAll(HttpMethod.DELETE, urls);
                result.putAll(HttpMethod.HEAD, urls);
                result.putAll(HttpMethod.PATCH, urls);
                continue;
            }
            // 根据请求方法，添加到 result 结果
            entry.getKey().getMethodsCondition().getMethods().forEach(requestMethod -> {
                switch (requestMethod) {
                    case GET:
                        result.putAll(HttpMethod.GET, urls);
                        break;
                    case POST:
                        result.putAll(HttpMethod.POST, urls);
                        break;
                    case PUT:
                        result.putAll(HttpMethod.PUT, urls);
                        break;
                    case DELETE:
                        result.putAll(HttpMethod.DELETE, urls);
                        break;
                    case HEAD:
                        result.putAll(HttpMethod.HEAD, urls);
                        break;
                    case PATCH:
                        result.putAll(HttpMethod.PATCH, urls);
                        break;
                }
            });
        }
        return result;
    }
```

2. 之后获取配置文件中的**yudao.security.permit-all-urls**属性获取到数组，可以按照接口位置进行放行，不校验。
3. 由于不同的服务都有不同的接口，如果所有的接口都在同一个位置进行单独处理，会导致代码冲突很多，同时维护起来也很麻烦（屎山）。可以尝试将这个权限控制下放到各个不同的服务，比如System-Server。

> 实现原理如下：
>
> 我们的**YudaoWebSecurityConfigurerAdapter**使用了自动注入，在类中有一个AuthorizeRequestsCustomizer的集合。其中依赖于Spring的自动扫描注入功能，所以我们如果新建了一个服务，可以通过创建一个Bean来创建这个访问规则，比如我们的System-Server模块，
>
> ```java
> @Configuration(proxyBeanMethods = false, value = "systemSecurityConfiguration")
> public class SecurityConfiguration {
>     @Bean("systemAuthorizeRequestsCustomizer")
>     public AuthorizeRequestsCustomizer authorizeRequestsCustomizer() {
>         return new AuthorizeRequestsCustomizer() {
>             @Override
>             public void customize(AuthorizeHttpRequestsConfigurer<HttpSecurity>.AuthorizationManagerRequestMatcherRegistry registry) {
>                 // TODO 芋艿：这个每个项目都需要重复配置，得捉摸有没通用的方案
>                 // Swagger 接口文档
>                 registry.requestMatchers("/v3/api-docs/**").permitAll()
>                         .requestMatchers("/webjars/**").permitAll()
>                         .requestMatchers("/swagger-ui").permitAll()
>                         .requestMatchers("/swagger-ui/**").permitAll();
>                 // Druid 监控
>                 registry.requestMatchers("/druid/**").permitAll();
>                 // Spring Boot Actuator 的安全配置
>                 registry.requestMatchers("/actuator").permitAll()
>                         .requestMatchers("/actuator/**").permitAll();
>                 // RPC 服务的安全配置
>                 registry.requestMatchers(ApiConstants.PREFIX + "/**").permitAll();
>             }
> 
>         };
>     }
> }
> ```
>
> 通过注入Bean：systemAuthorizeRequestsCustomizer，重写customize方法将放行方法通行。
>
> 之后通过在主类（YudaoWebSecurityConfigurerAdapter）中设置自定义规则（**authorizeHttpRequests(c -> authorizeRequestsCustomizers.forEach(customizer -> customizer.customize(c)))**），之后是必须要认证的接口URL。



### 三方登录

流程图如图所示：

![image-20260108004231128](images/yudao/image-20260108004231128.png)

## 框架组件

### 操作日志、访问日志、错误日志处理

#### 访问日志

我们定义了一个注解：**@ApiAccesLog**

```java
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ApiAccessLog {

    // ========== 开关字段 ==========

    /**
     * 是否记录访问日志
     */
    boolean enable() default true;
    /**
     * 是否记录请求参数
     *
     * 默认记录，主要考虑请求数据一般不大。可手动设置为 false 进行关闭
     */
    boolean requestEnable() default true;
    /**
     * 是否记录响应结果
     *
     * 默认不记录，主要考虑响应数据可能比较大。可手动设置为 true 进行打开
     */
    boolean responseEnable() default false;
    /**
     * 敏感参数数组
     *
     * 添加后，请求参数、响应结果不会记录该参数
     */
    String[] sanitizeKeys() default {};

    // ========== 模块字段 ==========

    /**
     * 操作模块
     *
     * 为空时，会尝试读取 {@link io.swagger.v3.oas.annotations.tags.Tag#name()} 属性
     */
    String operateModule() default "";
    /**
     * 操作名
     *
     * 为空时，会尝试读取 {@link io.swagger.v3.oas.annotations.Operation#summary()} 属性
     */
    String operateName() default "";
    /**
     * 操作分类
     *
     * 实际并不是数组，因为枚举不能设置 null 作为默认值
     */
    OperateTypeEnum[] operateType() default {};

}
```

之后我们定义一个过滤器：**ApiAccessLogFilter**，作用是在过滤器中拿到请求和响应进行参数处理。

```java
public class ApiAccessLogFilter extends ApiRequestFilter
```

这个类继承自ApiRequestFilter，下方就是父类实现方式，主要是过滤出只有API的接口。

```java
@RequiredArgsConstructor
public abstract class ApiRequestFilter extends OncePerRequestFilter {

    protected final WebProperties webProperties;

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        // 只过滤 API 请求的地址
        String apiUri = request.getRequestURI().substring(request.getContextPath().length());
        return !StrUtil.startWithAny(apiUri, webProperties.getAdminApi().getPrefix(), webProperties.getAppApi().getPrefix());
    }
}
```

之后在ApiRequestFilter中重写方法：

```java
    @Override
    @SuppressWarnings("NullableProblems")
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        // 获得开始时间
        LocalDateTime beginTime = LocalDateTime.now();
        // 提前获得参数，避免 XssFilter 过滤处理
        Map<String, String> queryString = ServletUtils.getParamMap(request);
        String requestBody = ServletUtils.isJsonRequest(request) ? ServletUtils.getBody(request) : null;

        try {
            // 继续过滤器
            filterChain.doFilter(request, response);
            // 正常执行，记录日志
            createApiAccessLog(request, beginTime, queryString, requestBody, null);
        } catch (Exception ex) {
            // 异常执行，记录日志
            createApiAccessLog(request, beginTime, queryString, requestBody, ex);
            throw ex;
        }
    }
```

> 在上述方法中，首先记录开始时间，之后进行`filterChain.doFilter(request, response);`处理，得到响应，正常情况下，在标准的Servlet中，`HttpServletResponse`只能输出流，拿不到Controller的`CommonResult`（统一返回结果类）的，所以需要一个全局返回对象处理类，`GlobalResponseBodyHandler`，代码如下：
>
> ```java
> @ControllerAdvice
> public class GlobalResponseBodyHandler implements ResponseBodyAdvice {
>     @Override
>     @SuppressWarnings("NullableProblems") // 避免 IDEA 警告
>     public boolean supports(MethodParameter returnType, Class converterType) {
>         if (returnType.getMethod() == null) {
>             return false;
>         }
>         // 只拦截返回结果为 CommonResult 类型
>         return returnType.getMethod().getReturnType() == CommonResult.class;
>     }
> 
>     @Override
>     @SuppressWarnings("NullableProblems") // 避免 IDEA 警告
>     public Object beforeBodyWrite(Object body, MethodParameter returnType, MediaType selectedContentType, Class selectedConverterType,
>                                   ServerHttpRequest request, ServerHttpResponse response) {
>         // 记录 Controller 结果
>         WebFrameworkUtils.setCommonResult(((ServletServerHttpRequest) request).getServletRequest(), (CommonResult<?>) body);
>         return body;
>     }
> }
> ```
>
> supports方法作用是：判断返回结果是不是CommonResult类型，如果不是就不需要处理。
>
> beforeBodyWrite方法作用是：向WebFrameworkUtils设置CommonResult结果，之后可以在过滤器中继续使用。
>
> 之后走正常执行的日志记录逻辑。

```java
    private void createApiAccessLog(HttpServletRequest request, LocalDateTime beginTime,
                                    Map<String, String> queryString, String requestBody, Exception ex) {
        ApiAccessLogCreateReqDTO accessLog = new ApiAccessLogCreateReqDTO();
        try {
            boolean enable = buildApiAccessLog(accessLog, request, beginTime, queryString, requestBody, ex);
            if (!enable) {
                return;
            }
            apiAccessLogApi.createApiAccessLogAsync(accessLog);
        } catch (Throwable th) {
            log.error("[createApiAccessLog][url({}) log({}) 发生异常]", request.getRequestURI(), toJsonString(accessLog), th);
        }
    }
```

上述方法就是在判断是否需要记录日志之后进行日志的记录同时需要构建accessLog参数。

下面介绍最重要的**buildApiAccessLog**判断是否记录日志的逻辑。

```java
private boolean buildApiAccessLog(ApiAccessLogCreateReqDTO accessLog, HttpServletRequest request, LocalDateTime beginTime,
                                      Map<String, String> queryString, String requestBody, Exception ex) {
        // 判断：是否要记录操作日志
        HandlerMethod handlerMethod = (HandlerMethod) request.getAttribute(ATTRIBUTE_HANDLER_METHOD);
        ApiAccessLog accessLogAnnotation = null;
        if (handlerMethod != null) {
            accessLogAnnotation = handlerMethod.getMethodAnnotation(ApiAccessLog.class);
            if (accessLogAnnotation != null && BooleanUtil.isFalse(accessLogAnnotation.enable())) {
                return false;
            }
        }

        // 处理用户信息
        accessLog.setUserId(WebFrameworkUtils.getLoginUserId(request))
                .setUserType(WebFrameworkUtils.getLoginUserType(request));
        // 设置访问结果
        CommonResult<?> result = WebFrameworkUtils.getCommonResult(request);
        if (result != null) {
            accessLog.setResultCode(result.getCode()).setResultMsg(result.getMsg());
        } else if (ex != null) {
            accessLog.setResultCode(GlobalErrorCodeConstants.INTERNAL_SERVER_ERROR.getCode())
                    .setResultMsg(ExceptionUtil.getRootCauseMessage(ex));
        } else {
            accessLog.setResultCode(GlobalErrorCodeConstants.SUCCESS.getCode()).setResultMsg("");
        }
        // 设置请求字段
        accessLog.setTraceId(TracerUtils.getTraceId()).setApplicationName(applicationName)
                .setRequestUrl(request.getRequestURI()).setRequestMethod(request.getMethod())
                .setUserAgent(ServletUtils.getUserAgent(request)).setUserIp(ServletUtils.getClientIP(request));
        String[] sanitizeKeys = accessLogAnnotation != null ? accessLogAnnotation.sanitizeKeys() : null;
        Boolean requestEnable = accessLogAnnotation != null ? accessLogAnnotation.requestEnable() : Boolean.TRUE;
        if (!BooleanUtil.isFalse(requestEnable)) { // 默认记录，所以判断 !false
            Map<String, Object> requestParams = MapUtil.<String, Object>builder()
                    .put("query", sanitizeMap(queryString, sanitizeKeys))
                    .put("body", sanitizeJson(requestBody, sanitizeKeys)).build();
            accessLog.setRequestParams(toJsonString(requestParams));
        }
        Boolean responseEnable = accessLogAnnotation != null ? accessLogAnnotation.responseEnable() : Boolean.FALSE;
        if (BooleanUtil.isTrue(responseEnable)) { // 默认不记录，默认强制要求 true
            accessLog.setResponseBody(sanitizeJson(result, sanitizeKeys));
        }
        // 持续时间
        accessLog.setBeginTime(beginTime).setEndTime(LocalDateTime.now())
                .setDuration((int) LocalDateTimeUtil.between(accessLog.getBeginTime(), accessLog.getEndTime(), ChronoUnit.MILLIS));

        // 操作模块
        if (handlerMethod != null) {
            Tag tagAnnotation = handlerMethod.getBeanType().getAnnotation(Tag.class);
            Operation operationAnnotation = handlerMethod.getMethodAnnotation(Operation.class);
            String operateModule = accessLogAnnotation != null && StrUtil.isNotBlank(accessLogAnnotation.operateModule()) ?
                    accessLogAnnotation.operateModule() :
                    tagAnnotation != null ? StrUtil.nullToDefault(tagAnnotation.name(), tagAnnotation.description()) : null;
            String operateName = accessLogAnnotation != null && StrUtil.isNotBlank(accessLogAnnotation.operateName()) ?
                    accessLogAnnotation.operateName() :
                    operationAnnotation != null ? operationAnnotation.summary() : null;
            OperateTypeEnum operateType = accessLogAnnotation != null && accessLogAnnotation.operateType().length > 0 ?
                    accessLogAnnotation.operateType()[0] : parseOperateLogType(request);
            accessLog.setOperateModule(operateModule).setOperateName(operateName).setOperateType(operateType.getType());
        }
        return true;
    }
```

> 如果没有注解的话或者是显式的指定enable = false，会直接返回false。
>
> 如果存在注解并且没有显示的指定false，获取响应的**CommonResult**，如果注解中的**responseEnable**属性设置成true，就需要将这个内容一并设置到数据库中，之后设置一些请求的参数（getTraceId、getRequestURI、getUserAgent等），之后获取接口类和接口方法的swagger注释：
>
> ```java
> Tag tagAnnotation = handlerMethod.getBeanType().getAnnotation(Tag.class);
> Operation operationAnnotation = handlerMethod.getMethodAnnotation(Operation.class);
> ```
>
> 其中的handlerMethod.getBeanType()是获取这个方法的bean类。getAnnotation是获取注解。getMethodAnnotation是获取方法上的注解。之后是在日志中是否处理敏感词一类的操作，个人感觉没有必要处理。如果需要处理的话，DFA算法处理，如果敏感词很多的话最好是使用定制方法，可控。Trie树（前缀树）、AC自动机。





## Spring Cloud 微服务调试

微服务的架构下，多服务的调试是非常大的痛点，大家使用同一个注册中心的时候，如果多个人在本地启动了相同的服务，调试的请求很可能会打到其他人的本地地址，实际上期望的是自己的服务。一般情况下都会在本地起一个注册中心，但是如果服务一旦多的话，本地电脑内存受不了。

项目中实现了一个模块：**spring-boot-starter-env**组件，通过tag给服务打标签，实现在同一个注册中心的情况下，本地只需要正常启动服务，保证自己的请求会打到自己的服务。

![image-20260111232943632](images/yudao/image-20260111232943632.png)

启动Gateway服务、System服务、Infra服务。观察nacos中的服务metadata。

gateway如下:

![image-20260111233253030](images/yudao/image-20260111233253030.png)

system服务如下：

![image-20260111233317120](images/yudao/image-20260111233317120.png)

#### 实现方法

在**application.properties**文件中添加：`liangzhichao.env.tag=${HOSTNAME}`，之后使用`org.springframework.boot.env`包下的内容，定义一个多环境实现类（用来做环境隔离，就是在环境变量中设置tag属性），代码实现如下：

```java
public class EnvEnvironmentPostProcessor implements EnvironmentPostProcessor {
    private static final Set<String> TARGET_TAG_KEYS = SetUtils.asSet(
            "spring.cloud.nacos.discovery.metadata.tag" // Nacos 注册中心
            // MQ TODO
    );
    @Override
    public void postProcessEnvironment(ConfigurableEnvironment environment, SpringApplication application) {
        // 0. 设置 ${HOST_NAME} 兜底的环境变量
        String hostNameKey = StrUtil.subBetween(HOST_NAME_VALUE, "{", "}");
        if (!environment.containsProperty(hostNameKey)) {
            environment.getSystemProperties().put(hostNameKey, EnvUtils.getHostName());
        }

        // 1.1 如果没有 yudao.env.tag 配置项，则不进行配置项的修改
        String tag = EnvUtils.getTag(environment);
        if (StrUtil.isEmpty(tag)) {
            return;
        }
        // 1.2 需要修改的配置项
        for (String targetTagKey : TARGET_TAG_KEYS) {
            String targetTagValue = environment.getProperty(targetTagKey);
            if (StrUtil.isNotEmpty(targetTagValue)) {
                continue;
            }
            environment.getSystemProperties().put(targetTagKey, tag);
        }
    }
}
```

>  EnvironmentPostProcessor是一个用于在Spring环境准备完成之后、应用上下文创建之前，对配置环境进行自定义处理。
>
> 启动流程：
>
> 1. SpringApplication.run()；
> 2. 环境准备时期：创建ConfigurableEnvironment对象。
> 3. 属性加载：加载application.yaml文件配置。
> 4. EnvironmentPostProcessor执行-自定义环境处理。
> 5. 应用上下文创建-创建ApplicationContext。
> 6. Bean加载和初始化-完成应用的启动。

由于这个EnvironmentPostProcessor的执行时机是在nacos执行之前，所以在nacos加载的时候可以做到侵入式的添加metadata = {tag}。

#### 网关转发过程

实现类：`GrayLoadBalancer`。

发现服务：

```java
 @Override
    public Mono<Response<ServiceInstance>> choose(Request request) {
        // 获得 HttpHeaders 属性，实现从 header 中获取 version
        HttpHeaders headers = ((RequestDataContext) request.getContext()).getClientRequest().getHeaders();
        // 选择实例
        ServiceInstanceListSupplier supplier = serviceInstanceListSupplierProvider.getIfAvailable(NoopServiceInstanceListSupplier::new);
        return supplier.get(request).next().map(list -> getInstanceResponse(list, headers));
    }
```

核心通过注册中心的**ServiceInstanceListSupplier**进行服务注册的发现，使用**get(Request)**发现服务。之后获取响应实例：

```java
    private Response<ServiceInstance> getInstanceResponse(List<ServiceInstance> instances, HttpHeaders headers) {
        // 如果服务实例为空，则直接返回
        if (CollUtil.isEmpty(instances)) {
            log.warn("[getInstanceResponse][serviceId({}) 服务实例列表为空]", serviceId);
            return new EmptyResponse();
        }

        // 筛选满足 version 条件的实例列表
        String version = headers.getFirst(VERSION);
        List<ServiceInstance> chooseInstances;
        if (StrUtil.isEmpty(version)) {
            chooseInstances = instances;
        } else {
            chooseInstances = CollectionUtils.filterList(instances, instance -> version.equals(instance.getMetadata().get("version")));
            if (CollUtil.isEmpty(chooseInstances)) {
                log.warn("[getInstanceResponse][serviceId({}) 没有满足版本({})的服务实例列表，直接使用所有服务实例列表]", serviceId, version);
                chooseInstances = instances;
            }
        }

        // 基于 tag 过滤实例列表
        chooseInstances = filterTagServiceInstances(chooseInstances, headers);

        // 随机 + 权重获取实例列表 TODO 芋艿：目前直接使用 Nacos 提供的方法，如果替换注册中心，需要重新失败该方法
        return new DefaultResponse(NacosBalancer.getHostByRandomWeight3(chooseInstances));
    }
```

下面是基于tag请求头，过滤匹配的服务实例列表：

```java
    private List<ServiceInstance> filterTagServiceInstances(List<ServiceInstance> instances, HttpHeaders headers) {
        // 情况一，没有 tag 时，过滤掉有 tag 的节点。目的：避免 test 环境，打到本地有 tag 的实例
        String tag = EnvUtils.getTag(headers);
        if (StrUtil.isEmpty(tag)) {
            List<ServiceInstance> chooseInstances = CollectionUtils.filterList(instances, instance -> StrUtil.isEmpty(EnvUtils.getTag(instance)));
            // 【重要】补充说明：如果希望在 chooseInstances 为空时，不允许打到有 tag 的实例，可以取消注释下面的代码
            if (CollUtil.isEmpty(chooseInstances)) {
                log.warn("[filterTagServiceInstances][serviceId({}) 没有不带 tag 的服务实例列表，直接使用所有服务实例列表]", serviceId);
                chooseInstances = instances;
            }
            return chooseInstances;
        }

        // 情况二，有 tag 时，使用 tag 匹配服务实例
        List<ServiceInstance> chooseInstances = CollectionUtils.filterList(instances, instance -> tag.equals(EnvUtils.getTag(instance)));
        if (CollUtil.isEmpty(chooseInstances)) {
            log.warn("[filterTagServiceInstances][serviceId({}) 没有满足 tag({}) 的服务实例列表，直接使用所有服务实例列表]", serviceId, tag);
            chooseInstances = instances;
        }
        return chooseInstances;
    }
```

最终会在**GrayReactiveLoadBalancerClientFilter**过滤器中将服务的地址进行替换：

```java
return choose(lbRequest, serviceId, supportedLifecycleProcessors).doOnNext(response -> {
                    if (!response.hasServer()) {
                        supportedLifecycleProcessors.forEach(lifecycle -> lifecycle
                                .onComplete(new CompletionContext<>(CompletionContext.Status.DISCARD, lbRequest, response)));
                        throw NotFoundException.create(properties.isUse404(), "Unable to find instance for " + url.getHost());
                    }

                    ServiceInstance retrievedInstance = response.getServer();

                    URI uri = exchange.getRequest().getURI();

                    // if the `lb:<scheme>` mechanism was used, use `<scheme>` as the default,
                    // if the loadbalancer doesn't provide one.
                    String overrideScheme = retrievedInstance.isSecure() ? "https" : "http";
                    if (schemePrefix != null) {
                        overrideScheme = url.getScheme();
                    }

                    DelegatingServiceInstance serviceInstance = new DelegatingServiceInstance(retrievedInstance,
                            overrideScheme);

                    URI requestUrl = reconstructURI(serviceInstance, uri);

                    if (log.isTraceEnabled()) {
                        log.trace("LoadBalancerClientFilter url chosen: " + requestUrl);
                    }
                    exchange.getAttributes().put(GATEWAY_REQUEST_URL_ATTR, requestUrl);
                    exchange.getAttributes().put(GATEWAY_LOADBALANCER_RESPONSE_ATTR, response);
                    supportedLifecycleProcessors.forEach(lifecycle -> lifecycle.onStartRequest(lbRequest, response));
                }).then(chain.filter(exchange))
                .doOnError(throwable -> supportedLifecycleProcessors.forEach(lifecycle -> lifecycle
                        .onComplete(new CompletionContext<ResponseData, ServiceInstance, RequestDataContext>(
                                CompletionContext.Status.FAILED, throwable, lbRequest,
                                exchange.getAttribute(GATEWAY_LOADBALANCER_RESPONSE_ATTR)))))
                .doOnSuccess(aVoid -> supportedLifecycleProcessors.forEach(lifecycle -> lifecycle
                        .onComplete(new CompletionContext<ResponseData, ServiceInstance, RequestDataContext>(
                                CompletionContext.Status.SUCCESS, lbRequest,
                                exchange.getAttribute(GATEWAY_LOADBALANCER_RESPONSE_ATTR),
                                new ResponseData(exchange.getResponse(), new RequestData(exchange.getRequest()))))));
```





































