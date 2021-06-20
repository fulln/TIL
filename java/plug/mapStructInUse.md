## mapStruct 开发使用

最近看到一个比较好的开发包`mapStruct` 这个对实现数据拷贝提供了一个简单的方式,可以用spring 或者静态变量的方式,对项目进行逻辑分层,代码分层提供了很方便的实现途径

### 使用

1. `pom`加载依赖

   ```
   <dependency>
       <groupId>org.mapstruct</groupId>
       <artifactId>mapstruct</artifactId>
       <version>${org.mapstruct.version}</version>
   </dependency>
   <!-- https://mvnrepository.com/artifact/org.mapstruct/mapstruct-processor -->
   <dependency>
       <groupId>org.mapstruct</groupId>
       <artifactId>mapstruct-processor</artifactId>
       <version>${org.mapstruct.version}</version>
   </dependency>
   ```

     此外,需要加载maven的`compiler` 插件

   ```
   <build>
       <plugins>
           <plugin>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-maven-plugin</artifactId>
           </plugin>
           <plugin>
               <groupId>org.apache.maven.plugins</groupId>
               <artifactId>maven-compiler-plugin</artifactId>
               <configuration>
                   <source>15</source>
                   <target>15</target>
                   <annotationProcessorPaths>
                       <path>
                           <groupId>org.projectlombok</groupId>
                           <artifactId>lombok</artifactId>
                           <version>${lombok.version}</version>
                       </path>
                       <path>
                           <groupId>org.mapstruct</groupId>
                           <artifactId>mapstruct-processor</artifactId>
                           <version>${org.mapstruct.version}</version>
                       </path>
                   </annotationProcessorPaths>
                   <compilerArgs>--enable-preview</compilerArgs>
               </configuration>
           </plugin>
       </plugins>
   </build>
   ```

2. 编写对应的转换实体和转换Mapper

   * `CarEntity`

     ```
     @Data
     public class CarDto{
         private String make;
         private Integer seatCount;
         private String type;
     }
     ```

   * `CarDTO`

     ```
     @Data
     public class CarDto{
         private String make;
         private Integer seatCount;
         private String type;
     }
     ```

   * `CarMapper`

      `CarMapper `有多种 实现方式,建议如果要使用Mapper的话,继承`org.springframework.core.convert.converter.Converter`,2个类的成员变量基本相同的情况下,可以不用做额外的方法处理,`Mapper`最常见的还是以下2种

     1.  声明为`SpringBean`
     2.  生成静态常量

       2种方式都行,代码如下

     ```
     @Mapper
     //@Mapper(componentModel = "spring") //第一种方式
     public interface CarMapper extends Converter<Car, CarDto> {
     	//第二种方式
         CarMapper MAPPER = Mappers.getMapper(CarMapper.class);
     
         @Mapping(target = "seatCount", source = "numberOfSeat")
         @Override
         CarDto convert(Car car);
     }
     ```

   * `test`

     测试类采用的第二种方式进行的转换,可见在使用方面还是比较方便的

     ```
     @Test
     public void transferTest(){
         Car car = new Car();
         car.setMake("转换测试");
         car.setNumberOfSeat(11);
         car.setType("dd");
         System.out.println(car);
         CarDto convert = CarMapper.MAPPER.convert(car);
         System.out.println(convert);
     }
     ```


### 进阶使用方式
下面选择几个常用场景描述下

1. 多参数
```java
@Mapper
public interface AddressMapper {

    @Mapping(source = "person.description", target = "description")
    @Mapping(source = "address.houseNo", target = "houseNumber")
    DeliveryAddressDto personAndAddressToDeliveryAddressDto(Person person, Address address);
}
```

2. 使用spring管理,不写常量类
```java
@Mapper(componentModel = "spring")
public interface CarMapper {

    CarDto carToCarDto(Car car);
}
```

3.调用其他的映射
```java
@Mapper(uses=DateMapper.class)
public class CarMapper {

    CarDto carToCarDto(Car car);
}
```
4. 直接将mapper中返回的值转换出去
```java
@Repository // CDI component model
public class ReferenceMapper {

    @PersistenceContext
    private EntityManager entityManager;

    public <T extends BaseEntity> T resolve(Reference reference, @TargetType Class<T> entityClass) {
        return reference != null ? entityManager.find( entityClass, reference.getPk() ) : null;
    }

    public Reference toReference(BaseEntity entity) {
        return entity != null ? new Reference( entity.getPk() ) : null;
    }
}

@Mapper(componentModel = "cdi", uses = ReferenceMapper.class )
public interface CarMapper {

    Car carDtoToCar(CarDto carDto);
}

```

5. 指定字段使用指定方法转换
```java
@Mapper( uses = Titles.class )
public interface MovieMapper {

     @Mapping( target = "title", qualifiedByName = { "TitleTranslator", "EnglishToGerman" } )
     GermanRelease toGerman( OriginalRelease movies );

}
@Named("TitleTranslator")
public class Titles {

    @Named("EnglishToGerman")
    public String translateTitleEG(String title) {
        // some mapping logic
    }

    @Named("GermanToEnglish")
    public String translateTitleGE(String title) {
        // some mapping logic
    }
}

```

## 总结 

mapstruct 还是在开源项目中很经常使用,所以熟练使用还是对开发效率有很大的帮助
