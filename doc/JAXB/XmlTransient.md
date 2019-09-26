### 通过注解@XmlTransient改变Marshal的行为
背景：通过JAXB技术，使XML转成对象，或者使对象转成XML的过程，我们会有抹去一些字段映射的需求。

案例：有下面类型定义。其中我们想将Customer实例转成XML文档，其中Customer,Address,PhoneNumber都有id这个字段。我希望转换的结果中不包含id。
```
@Getter
@Setter
public class Base {
    private int id;
}
```
```
@Getter
@Setter
@XmlRootElement
public class Customer extends Base {
    private String name;
    private Address address;
    private List<PhoneNumber> phoneNumbers;
}
```
```
@Getter
@Setter
public class Address extends Base {
    private String street;
}
```
```
@Getter
@Setter
public class PhoneNumber extends Base {
    private String number;
}
```
正常情况下我们会得到下面的结果。
``` xml
<customer>
    <id>99</id>
    <address>
        <id>34</id>
        <street>wuhe</street>
    </address>
    <name>good</name>
    <phoneNumbers>
        <id>12</id>
        <number>123</number>
    </phoneNumbers>
</customer>
```
但是下面所示才是我想要生成结果。
``` xml
<customer>
    <address>
        <street>wuhe</street>
    </address>
    <name>good</name>
    <phoneNumbers>
        <number>123</number>
    </phoneNumbers>
</customer>
```
该如何做才行呢？此时可以用@XmlTransient这个注解来实现目的。XmlTransient可以用在三种目标上，如下所示。
- a JavaBean property
- field
- class

# One
用在不同的对象上效果是不一样。基于我们的需求，我们要用到的是第一种，也就是a JavaBean property。它表示的意思是阻止property映射到XML。
当XmlTransient用在property上的时候，需要放在get方法上才能生效，所以我们将Base改造如下：
```
public class Base {
    private int id;

    @XmlTransient
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }
}
```
这个时候我们就能得到没有id节点的XML文档。
# Two
其他：上面的案例是XmlTransient用在property上的场景。那么什么时候需要将其应用到class或者field上呢？
- 首先讲讲class。
    ```
    @Getter
    @Setter
    @XmlTransient
    public class Base {
        private int id;
    }
    ```
    结果会抛出下面的异常。这是因为XmlTransient用在class上的时候，表示这个class不能直接被映射成XML。
    ```
    Exception in thread "main" javax.xml.bind.JAXBException: class net.skyscanner.fbipartners.stratolaunch.api.Base nor any of its super class is known to this context.
    ```
- 再说说field。
    XmlTransient用在field上的时候主要是用来解决冲突的。如下，我们把id改成public，那么JAXB就会认为Base中有两个同名的定义。
    一个是field id，一个是property id，存在同名冲突。这个时候将XmlTransient放置于id或者getId上都可。当然这里放置在getId上
    相当于是XmlTransient用在property。

    ```
    public class Base {
        @XmlTransient
        public int id;
    
        public int getId() {
            return id;
        }
        public void setId(int id) {
            this.id = id;
        }
    }
    or
    public class Base {
        public int id;
        @XmlTransient
        public int getId() {
            return id;
        }
        public void setId(int id) {
            this.id = id;
        }
    }    
    ```