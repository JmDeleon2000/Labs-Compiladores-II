# Failed build example:
```{yapl}
class foo inherits goo
{
    yt : Int;
    fasdf(x:String, y:Goo ):Int
    {
        h <- 15 + "bar";
        h <-"foo" + 6;
        h <-"foo" / 6;
        h <-"foo" * 6;
        h <-"foo" - 6;
        h <-15 + 6;
        h <-15 / 6;
        h <-15 * 6;
        h <-15 - 6;
    };

};
```
<span style = "color:red">
Unsupported operation between int and string for operator +: 15+"bar"</br>
Unsupported operation between string and int for operator +: "foo"+6</br>
Unsupported operation between string and int for operator /: "foo"/6</br>
Unsupported operation between string and int for operator *: "foo"*6</br>
Unsupported operation between string and int for operator -: "foo"-6</br>
Build fail. Found errors.
</span>


# Successful build example:
```{yapl}
class foo inherits goo
{
    yt : Int;
    fasdf(x:String, y:Goo ):Int
    {
        h <-15 + 6;
        h <-15 / 6;
        h <-15 * 6;
        h <-15 - 6;
    };

};
```
<span style = "color:green">
Build success
</span>