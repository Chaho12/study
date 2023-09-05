# Check

> Please check out the medium post for more details.
> This page only reviews those that are not intuitive nor simple

## Use comments sparingly

Comments should be used only when necessary and should be clear and concise. Overuse of comments can clutter the code and make it harder to read. For example:

```c
// Bad Example
// This function adds two numbers together and returns the result
public int add(int num1, int num2)
{
    // add the numbers together
    int result = num1 + num2;
    // return the result
    return result;
}

// Good Example
public int Add(int firstNumber, int secondNumber)
{
    int result = firstNumber + secondNumber;
    return result;
}
```

## Write small, focused methods:

Methods should be small and focused, with a single responsibility. This makes the code easier to understand and modify. For example:

```c
// Bad Example
public void DoEverything(int x, int y, int z)
{
    // do something
    // do something else
    // and more
}

// Good Example
public int Add(int firstNumber, int secondNumber)
{
    return firstNumber + secondNumber;
}

public int Multiply(int firstNumber, int secondNumber)
{
    return firstNumber * secondNumber;
}
```

## Use inheritance and polymorphism:

Inheritance and polymorphism can make the code more flexible and easier to modify. For example:

```c
// Bad Example
public class Animal
{
    public void Walk()
    {
        // walk
    }
}

public class Dog
{
    public void Walk()
    {
        // walk
    }

    public void Bark()
    {
        // bark
    }
}

// Good Example
public abstract class Animal
{
    public abstract void Walk();
}

public class Dog : Animal
{
    public override void Walk()
    {
        // walk
    }

    public void Bark()
    {
        // bark
    }
}
```

## Use descriptive error messages:

Error messages should be clear and descriptive, to help developers understand the problem and how to fix it. For example:

```c
// Bad Example
public void CalculateTotal(decimal price, int quantity)
{
    if (price < 0 || quantity < 0)
    {
        throw new Exception("Invalid input");
    }
    // calculate total
}

// Good Example
public void CalculateTotal(decimal price, int quantity)
{
    if (price < 0)
    {
        throw new ArgumentException("Price cannot be negative", nameof(price));
    }
    if (quantity < 0)
    {
        throw new ArgumentException("Quantity cannot be negative", nameof(quantity));
    }
    // calculate total
}
```

## Keep methods small:

Small methods are easier to understand, test, and modify. It is important to break down larger methods into smaller, focused methods that do one thing and do it well. For example:

```c
// Bad Example
public void SaveData(string data)
{
    if (data == null)
    {
        throw new ArgumentNullException(nameof(data));
    }
    if (data.Length > 100)
    {
        throw new ArgumentException("Data length cannot exceed 100 characters", nameof(data));
    }
    if (File.Exists("data.txt"))
    {
        File.Delete("data.txt");
    }
    File.WriteAllText("data.txt", data);
}

// Good Example
public void SaveData(string data)
{
    ValidateData(data);
    DeleteExistingFile("data.txt");
    WriteFile("data.txt", data);
}

private void ValidateData(string data)
{
    if (data == null)
    {
        throw new ArgumentNullException(nameof(data));
    }
    if (data.Length > 100)
    {
        throw new ArgumentException("Data length cannot exceed 100 characters", nameof(data));
    }
}

private void DeleteExistingFile(string fileName)
{
    if (File.Exists(fileName))
    {
        File.Delete(fileName);
    }
}

private void WriteFile(string fileName, string data)
{
    File.WriteAllText(fileName, data);
}
```

## Source

https://medium.com/@shubhadeepchat/best-practices-for-clean-code-aaba4a4832bc
