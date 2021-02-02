## mapStruct 开发使用

最近看到一个比较好的开发包`mapStruct` 这个对实现数据拷贝提供了一个简单的方式,可以用spring 或者静态变量的方式,对项目进行逻辑分层,代码分层提供了很方便的实现途径

### 使用方式

1. 引入pom
```java
	<dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct-jdk8</artifactId>
            <version>1.3.0.Final</version>
        </dependency>
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct-processor</artifactId>
            <version>1.3.0.Final</version>
        </dependency>
```

后面的包是为了在🧬的时候就展示对应的实现类到本地

2. 使用demo
```java
@Mapper 1
public interface CarMapper {
	 
    CarMapper INSTANCE = Mappers.getMapper( CarMapper.class ); 3
    // 将car 转换为 carDTO
    @Mapping(source = "numberOfSeats", target = "seatCount")
    CarDto carToCarDto(Car car); 2
}

public class Car {
 
    private String make;
    private int numberOfSeats;
    private CarType type;
 
    //constructor, getters, setters etc.
}

public class CarDto {
 
    private String make;
    private int seatCount;
    private String type;
 
    //constructor, getters, setters etc.
}
```
然后使用

```java
@Test
public void shouldMapCarToDto() {
    //given
    Car car = new Car( "Morris", 5, CarType.SEDAN );
 
    //when
    CarDto carDto = CarMapper.INSTANCE.carToCarDto( car );
 
    //then
    assertThat( carDto ).isNotNull();
    assertThat( carDto.getMake() ).isEqualTo( "Morris" );
    assertThat( carDto.getSeatCount() ).isEqualTo( 5 );
    assertThat( carDto.getType() ).isEqualTo( "SEDAN" );
}
```
就可以轻易的转换了,不用自己手动写对应的转换

### 常用方式
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


## 总结 

mapstruct 还是在开源项目中很经常使用,所以熟练使用还是对开发效率有很大的帮助
