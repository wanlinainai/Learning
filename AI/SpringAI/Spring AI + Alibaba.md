# SpringAI + SpringAI Alibaba

## 工具调用

1. 使用过程中，在聊天请求中包含其定义。每一个工具的定义包含了名称、描述和输入参数的架构。对应@Tool中就是：name、description
2. 模型决定调用工具的时候，发送一个包含工具名称和按照定义架构建模的输入参数的响应。
3. 应用名称负责使用工具名称来识别和执行具有提供输入参数的 工具。
4. 工具调用的结果由应用程序处理。
5. 应用程序将结果发送给模型。
6. 模型使用工具调用结果作为额外上下文生成最终响应。

```java
@Slf4j
public class DateTimeTools {

    /**
     * 获取当前时间的工具
     * @return
     */
    @Tool(description = "Get the current date and time in the user's timezone")
    String getCurrentDateTime() {
//        log.warn("Tool is used...");
        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
    }

    /**
     * 设置闹钟工具，注意：需要加上jsonschema的maven依赖，否则报错：Handler dispatch failed: java.lang.NoClassDefFoundError: com/github/victools/jsonschema/generator/AnnotationHelper
     * 依赖部分见：POM中的：jsonschema-generator、jsonschema-module-jackson
     * @param time
     */
    @Tool(description = "Set a user alarm for the given time, provided in ISO-8601 format")
    void setAlarm(String time) {
        LocalDateTime alarmTime = LocalDateTime.parse(time, DateTimeFormatter.ISO_DATE_TIME);
        log.warn("Alarm set for :" + alarmTime);
    }
}
```

```java
@RestController
@RequestMapping("/chat")
@Slf4j
public class ChatController {
    private final ChatClient chatClient;

    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    /**
     * 日期工具调用
     */
    @GetMapping("/getCurrentDateTime")
    public String getCurrentDateTime(@RequestParam(value = "query", defaultValue = "现在是几点") String query) {
        log.info("用户输入：【" + query + "】");
        String content = chatClient.prompt(query)
                .tools(new DateTimeTools())
                .call()
                .content();
        log.info("AI回复：【" + content + "】");
        return content;
    }
}
```

调用：`http://localhost:9088/chat/getCurrentDateTime?query="现在几点了，帮我设置一个10分钟之后的闹钟"`。如果报错：系统异常: Handler dispatch failed: java.lang.NoClassDefFoundError: com/github/victools/jsonschema/generator/AnnotationHelper。需要添加依赖：

```xml
        <dependency>
            <groupId>com.github.victools</groupId>
            <artifactId>jsonschema-generator</artifactId>
            <version>4.30.0</version>
        </dependency>
        <dependency>
            <groupId>com.github.victools</groupId>
            <artifactId>jsonschema-module-jackson</artifactId>
            <version>4.30.0</version>
        </dependency>
```

































