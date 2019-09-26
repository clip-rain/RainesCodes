# We can use Annotation XmlJavaTypeAdapter to change the behavior of Marshaller or Unmarshaller.
 

- [We can't Use XmlAdapter without @XmlJavaTypeAdapter](https://stackoverflow.com/questions/6857166/jaxb-isnt-it-possible-to-use-an-xmladapter-without-xmljavatypeadapter)

- Define a Adapter which is inherit from XmlAdapter.
    
    ```
    public class SillyDate {
        public SillyDate(int year, int month, int day) {
            super();
            this.year = year;
            this.month = month;
            this.day = day;
        }
    
        public String toString() {
          return "SillyDate [year=" + year + ", month=" + month + ", day=" + day + "]";
        }
    
        public int year;
        public int month;
        public int day;
    }
    ```
    ```
    public class SillyDateAdapter extends XmlAdapter<XMLGregorianCalendar, SillyDate> {
        public SillyDate unmarshal(XMLGregorianCalendar val) throws Exception {
          return new SillyDate(val.getYear(), val.getMonth(), val.getDay());
        }
    
        public XMLGregorianCalendar marshal(SillyDate val) throws Exception {
          return DatatypeFactory.newInstance().newXMLGregorianCalendarDate(val.year, val.month, val.day, 0);
        }
    }
    ```
    ```
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlRootElement
    public class Example {
        @XmlSchemaType(name = "date")
        @XmlJavaTypeAdapter(type=XMLGregorianCalendar.class,value =SillyDateAdapter.class)
        public SillyDate publishingDate;
    }
 
    ```
    
    
- Unmarshal to subclass of marshaled class. [stack overflow](https://stackoverflow.com/questions/619761/jaxb-inheritance-unmarshal-to-subclass-of-marshaled-class)

    ```
    public class YourNiceAdapter extends XmlAdapter<ReceiverPerson,Person>{

        @Override public Person unmarshal(ReceiverPerson v){
            return v;
        }
        @Override public ReceiverPerson marshal(Person v){
            return new ReceiverPerson(v); // you must provide such c-tor
        }
    }
    ```
    ```
    @Your_favorite_JAXB_Annotations_Go_Here
    class SomeClass{
        @XmlJavaTypeAdapter(YourNiceAdapter.class)
        Person hello; // field to unmarshal
    }
    ```
    
- Unfortunately, if there are multiple subclass of the marshaled class, I can't use the Adapter to change the unmarshal process.
I found another way to do this. We can use [@XmlAnyElement annotation](./XmlAnyElement.md) to unmarshal the xml to a subclass which we put in the JAXBContext.

