# Running Java classes

### No package, same directory
Open command prompt and change directory to TestClassPath. If TestClassPath is in `C:\Users\Cat\TestClassPath`, then:

`cd C:\Users\Cat\TestClassPath` 

If your class is not in any package, like this Hello.java, then simply, compile and run it:

```
> javac Hello.java
> java Hello
```

### Class in package
In this example, HelloCat.java is in `com.cat` package, and is inside `com\cat` directory (Notice the directory naming follows the package naming). To run in, you must specify the package name before the HelloCat class name:

```
> javac com\cat\HelloCat.java
> java com.cat.HelloCat
```

### Class in package and in different dir than current dir
After you compile the code, if your .class cannot be reached from current directory, you have to set CLASSPATH variable.

Suppose we're currently in `C:\Users\Cat\TestClassPath` and we have `com.cat.HelloCatBox` located in the box folder

`C:\Users\Cat\TestClassPath\box\com\cat\HelloCatBox.java`

Then if we want to run `com.cat.HelloCatBox` from the TestClassPath directory. Compile it: (box here is not a package name, just a directory where it contains com.cat.HelloCat):

```
> javac box\com\cat\HelloCatBox.java
```

We can use -cp to let Java runtime know where to look for the class file. If we dun do that, we will encounter this:

`Error: Could not find or load main class com.cat.HelloCatBox`

So we have to set the classpath and let Java runtime knows that com.cat.HelloCatBox is in 'box' folder
```
> java -cp box com.cat.HelloCatBox
```
