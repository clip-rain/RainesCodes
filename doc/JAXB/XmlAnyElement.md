# What do this annotation mean?
Maps a JavaBean property to XML infoset representation and/or JAXB element.
This annotation serves as a "catch-all" property while unmarshalling 
xml content into a instance of a JAXB annotated class. It typically
annotates a multi-valued JavaBean property, but it can occur on
single value JavaBean property. During unmarshalling, each xml element 
that does not match a static &#64;XmlElement or &#64;XmlElementRef 
annotation for the other JavaBean properties on the class, is added to this 
"catch-all" property.

# When should use this?
In some scenario, I define a super class. But I want to unmarshal XML to one of its 
subclass.We can use this to reach our purpose. Sure, there are some limits when we use @XmlAnyElement to 
unmarshal XML to one of the subclass. Those limits are below:
- You should put @XmlAnyElement on only one property in the same class.
- When you put @XmlAnyElement on one property, it means that this property can handle the 
unmatched nodes in XML.
- You have to put the type of real subclass in the JAXBContext. So it means that, if you want to
unmarshal to different subclass, you should define different JAXBContext.

```
@XmlRootElement
@Getter
@Setter
@XmlAccessorType(XmlAccessType.FIELD)
public class Message {
    private String name;

    @XmlAnyElement(lax=true)
    private BaseBody body;
}
```
```
public class BaseBody {
}
```

```
@XmlRootElement
@Getter
@Setter
public class Phone extends BaseBody {
    private String number;
}

```

```
@Getter
@Setter
@XmlRootElement
public class House extends BaseBody {
    private String street;
    private String city;
}
```

``` 
test1.xml
<message>
    <name>leiyu</name>
    <phone>
        <number>1234</number>
    </phone>
</message>

```

``` 
test2.xml
<message>
    <name>leiyu</name>
    <house>
        <street>123 A Street</street>
        <city>Any Town</city>
    </house>
</message>

```

```
JAXBContext jax = JAXBContext.newInstance(Message.class, House.class, Phone.class);
Unmarshaller unmarshaller = jax.createUnmarshaller();
String re = Resources.toString(Resources.getResource("test.xml"), Charsets.UTF_8);
Message mm = (Message) unmarshaller.unmarshal(new StringInputStream(re));
```

See the above codes, I put @XmlAnyElement(lax=true) on the `body` property in Message class.
And I put the type of House and Phone into the JAXBContext. And I can unmarshal the test1.xml
and test2.xml at the same time.

Keep mind that, if we want to unmarshal XML to a property, we have to define a getter for
this property and add the @XmlAccessorType(XmlAccessType.FIELD) to the class which the property
belong.(sure, you can use @XmlTransient to reach the same purpose) 
`But for attribute, there is no need to add a getter for it.`



