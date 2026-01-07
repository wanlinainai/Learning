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













































