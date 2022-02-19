# Creating and Destroying Objects

## Item 1: Consider static factory methods instead of constructors

Static factory method: `static method that returns an instance of the class`.

```JAVA
// This method translates a boolean primitive value into a Boolean object reference:
public static Boolean valueOf(boolean b) {
    return b ? Boolean.TRUE : Boolean.FALSE;
}
```

ex1)

```java
// String Class constructor to create a string object
String value = new String("Baeldung");

// create a new String object static factory method -> name expresses pretty clearly what the method does. 
String value1 = String.valueOf(1);
String value2 = String.valueOf(1.0L);
String value3 = String.valueOf(true);
String value4 = String.valueOf('a');

```

ex2)

```java
Collection syncedCollection = Collections.synchronizedCollection(originalCollection);
Set syncedSet = Collections.synchronizedSet(new HashSet());
List<Integer> unmodifiableList = Collections.unmodifiableList(originalList);
Map<String, Integer> unmodifiableMap = Collections.unmodifiableMap(originalMap);
```

ex3)

```java
// Hiding from the client (better encapsulation) of object creation
public class UserFactory {

    public static User newUser(UserEnum type){
        switch (type){
            case ADMIN: return new Admin();
            case STAFF: return new StaffMember();
            case CLIENT: return new Client();
            default:
                throw new IllegalArgumentException("Unsupported user. You input: " + type);
        } 
    }
}

// client code - give me an admin object, 
// don't care about the inner details of how it gets constructed
User admin = UserFactory.newUser(ADMIN); 

// Flexibility to swap out implementations without breaking client code
// swap out with LinkedList later if you like, 
// it won't break the 100 places that invoke this method
public static List<String> getMyList(){
    return new ArrayList<>(); 
}

public class MyMuchBetterList<E> extends AbstractList<E> implements List<E> {
    // implementation
}

// swap inside the static factory without affecting those using getMyList:
public static List<String> getMyList(){
    return new MyMuchBetterList<>(); // compiles and works, subtype of list
}

```

ex4)

```java
public class User {
    
    private final String name;
    private final String email;
    private final String country;
    
    public User(String name, String email, String country) {
        this.name = name;
        this.email = email;
        this.country = country;
    }
    
    // standard getters / toString
}

// static factory method instead
public static User createWithDefaultCountry(String name, String email) {
    return new User(name, email, "Argentina");
}

// User instance with a default value assigned to the country field
User user = User.createWithDefaultCountry("John", "john@domain.com");
```

### Pros and Cons

#### Pros

1. Static factory methods have names. Constructors don't have meaningful names, so they are always restricted to the standard naming convention imposed by the language. (ex1)

    A class can have only a `single constructor` with a given signature. Programmers have been known to get around this restriction by providing two constructors whose parameter lists differ only in the order of their parameter types. This is a `really bad idea`. The `user of such an API` will never be able to remember which `constructor` is which and will end up calling the wrong one by mistake.

2. Static factory are not required to create a new object each time they’re invoked. (ex2)

    This allows immutable classes (Item 17) to use preconstructed instances, or to cache instances as they’re constructed, and dispense them repeatedly to avoid creating unnecessary duplicate objects. The Boolean.valueOf(boolean) method illustrates this technique: it never creates an object. It can greatly improve performance if equivalent objects are requested often, especially if they are expensive to create.

    The ability of static factory methods to return the same object from repeated invocations allows classes to maintain strict control over what instances exist at any time. -> Instance-controlled class.

    - Allows a class to guarantee that it is a singleton (Item 3) or noninstantiable (Item 4).
    - Allows an immutable value class (Item 17) to make the guarantee that no two equal instances exist: a.equals(b) if and only if a == b.

3. Static factory can return an object of any subtype of their return type. (ex3) as of java 8.

    - Hiding from the client (better encapsulation) of object creation
    - Flexibility to swap out implementations without breaking client code

4. Class of the returned object can vary from call to call as a function of the input parameters (ex4)

    The EnumSet class (Item 36) has no public constructors, only static factories. In the OpenJDK implementation, they return an instance of one of two subclasses, depending on the size of the underlying enum type: if it has sixty-four or fewer elements, as most enum types do, the static factories return a RegularEnumSet instance, which is backed by a single long; if the enum type has sixty-five or more elements, the factories return a JumboEnumSet instance, backed by a long array

5. Class of the returned object need not exist when the class containing the method is written (ex4)

    Such flexible static factory methods form the basis of service provider frameworks, like the Java Database Connectivity API (JDBC). A service provider framework is a system in which providers implement a service, and the system makes the implementations available to clients, decoupling the clients from the implementations.

#### Cons

1. limitation of providing only static factory methods is that classes without public or protected constructors cannot be subclassed.

2. Hard for programmers to find. They do not stand out in API documentation in the way that constructors do, so it can be difficult to figure out how to instantiate a class that provides static factory methods instead of constructors.

### References

<https://www.baeldung.com/java-constructors-vs-static-factory-methods>
<https://stackoverflow.com/questions/58719293/static-factory-methods-return-any-subtype>
