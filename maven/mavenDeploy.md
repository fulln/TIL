## 上传jar包到本地maven库

在你需要上传的pom文件里面设置:
```xml
<distributionManagement>
        <repository>
            <id>localRepository</id>
            <url>file:/path/to/you</url>
        </repository>
    </distributionManagement>
```
然后再执行`maven deploy` 就能将jar包传到本地的maven库

### 上传到自己搭的nexus

上面的pom文件设置改为

```xml
                <snapshotRepository>
                    <id>{your.id}</id>
                    <url>{your.url}</url>
                </snapshotRepository>
                <repository>
                    <id>{your.id}</id>
                    <url>{your.url}</url>
                </repository>
```

然后在maven的setting.xml文件中进行添加验证的用户名密码，就可以上传了




