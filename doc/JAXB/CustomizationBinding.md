We have two way to customize the binding of JAXB. The detail can be found in this page [Customize JAXB](https://docs.oracle.com/javase/tutorial/jaxb/intro/custom.html).

- Internal Binding <br/>
    - 

- External Binding
    - [Note that this customization is per namespace](https://javaee.github.io/jaxb-v2/doc/user-guide/ch03.html#customization-of-schema-compilation-customizing-java-packages) . That is, even if your schema is split into multiple schema documents, you cannot put them into different packages if they are all in the same namespace.
    - XMLBeans by default converts all XSD date and date time elements to a Java Calendar object. With JAXB however, by default the XMLGregorianCalendar is used. Yet again the global bindings came to the rescue and this was handled with the below configuration which converted all XSD date elements to a Java Calendar object.
        ``` xml
        <jxb:bindings 
        xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:jxb="http://java.sun.com/xml/ns/jaxb"
        jxb:extensionBindingPrefixes="xjc"
        version="2.1">
            <jxb:globalBindings>
               <jxb:javaType name="java.util.Calendar" xmlType="xs:dateTime"
                        parseMethod="javax.xml.bind.DatatypeConverter.parseDateTime"
                        printMethod="javax.xml.bind.DatatypeConverter.printDateTime"/>
                    <jxb:javaType name="java.util.Calendar" xmlType="xs:date"
                        parseMethod="javax.xml.bind.DatatypeConverter.parseDate"
                        printMethod="javax.xml.bind.DatatypeConverter.printDate"/>
                    <jxb:javaType name="java.util.Calendar" xmlType="xs:time"
                        parseMethod="javax.xml.bind.DatatypeConverter.parseTime"
                        printMethod="javax.xml.bind.DatatypeConverter.printTime"/>
            </jxb:globalBindings>
        </jxb:bindings>
        ```
    - [Syntax](https://docs.oracle.com/javase/tutorial/jaxb/intro/custom.html#bnbcm).