# Iris

Iris is a lightweight library that specialises on working with color.
The package does not rely on any third-party dependencies.

# Color class
Iris provides a handy Color class that is used to work with any given color.
This class stores the color in HSV color space and allows the end user the greater
flexibility while modifying the color.

## Creating a Color class using HSV values
Since the Color class uses HSV, the default constructor is set up to accept HSV values directly:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color(hue, saturation, value)
```
You can also use the built-in function `Color.from_hsv()` to construct the Color object. 
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
```
In this case, both methods are equivalent. The latter was added for the sake of consistensy with the other constructors.

## Creating a Color object using RGB values
The Color object provides a `Color.from_rgb()` function which can be used to create Color object from RGB band values, like this:
```python
from iris import Color

r, g, b = 100, 0, 255

c = Color.from_rgb(r, g, b)
```

## Creating a Color object using CMYK values
In case you need to create a Color object from CMYK values, you can use the `Color.from_cmyk()` method:
```python
from iris import Color

c, m, y, k = 15, 0, 45, 2

c = Color.from_cmyk(c, m, y, k)
```
Note that CMYK values should be integers in range [0..100], not floats. For example, a CMYK color defined as (45%, 11%, 0%, 56%) should be passed as `c=45, m=11, y=0, k=56`

## Creating a Color object using a hex-string
If you have a hex-string you can use the built-in `Color.from_hex()` method to create a Color object:
```python
from iris import Color

my_hex_str = "#00FF56"

c = Color.from_hex(my_hex_str)
```
Note that `Color.from_hex()` method only accepts a 7-symbol hex-string (a pound sign, 2 symbold for red, 2 symbols for green, 2 symbols for blue). Other variations, such as ARGB, are not supported.

## Representing the color as HSV
Since the HSV space is the space that the Color object uses to store data, no conversion is necessary.
To represent the color as HSV values, simply call the `Color.as_hsv()` method:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
hsv_tuple = c.as_hsv()
```
This method returns a tuple with the signature `(hue_value, saturation_value, value_value)`

## Representing the color as RGB
To convert the current color to RGB, simply call the `Color.as_rgb()` method:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rgb_tuple = c.as_rgb()
```
This method returns a tuple with the signature `(r_value, g_value, b_value)`.

## Representing the color as CMYK
To convert the current color to CMYK, call the `Color.as_cmyk()` method:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
cmyk_tuple = c.as_cmyk()
```
This method returns a tuple with the signature `(c_value, m_value, y_value, k_value)`. Note that these values are integers in range [0..100].

## Altering the hue of the color
To alter the color's hue, use the `Color.hue_shift()` method. The method takes a required positional argument `amount: int`, whic specifies the amount in degrees on a color wheel that the hue will be shifted by.

For example, this code will shift the color's hue by 30 degrees clockwise:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.hue_shift(30)
print(c.as_hsv()) # (290, 90, 90)
```
You can also pass a negative integer into the method to shift the hue counterclockwise. For example, the code below shifts the color's hue by 60 degress counterclockwise:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.hue_shift(-60)
print(c.as_hsv()) # (200, 90, 90)
```
Since the hue is always in range [0..360], the method will account for this. An example:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.hue_shift(120) # The shift has caused the hue to become out of acceptable range
# The hue is a representation of a color wheel, which cannot be more than 360deg, so the method has corrected the hue
print(c.as_hsv()) # (20, 90, 90)
```
The same logic works for negative shifts.

## Altering the saturation of the color
To alter the color's saturation, use the `Color.adjust_saturation()` method. It taked a required positional argument `amount: int`, that indicated the amount that the saturation needs to be adjusted by.

For example, this code below raises the color's saturation by 5%:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.adjust_saturation(5)
print(c.as_hsv()) # (260, 95, 90)
```
You can also pass a negative integer to lower the saturation level:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.adjust_saturation(-10)
print(c.as_hsv()) # (260, 80, 90)
```
Since the saturation level should always be in range [0..100], the method will cap any excessive adjustment:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.adjust_saturation(60000)
# The saturation has only been raised by 10 due to it being capped
print(c.as_hsv()) # (260, 100, 90)
```

## Altering the color's value
To adjust color's value, use the `Color.lighten()` and `Color.darken()` methods to lighten and darken the color respectively:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.lighten(10)
print(c.as_hsv()) # (200, 90, 100)
```
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.darken(60)
print(c.as_hsv()) # (260, 90, 30)
```
These methods do accept negative integers. In that case their functionality is reversed.
Since the value should always be in range [0..100], the method will cap any excessive adjustment:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.lighten(10000)
print(c.as_hsv()) # (200, 90, 100)
```
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.darken(600000)
print(c.as_hsv()) # (260, 90, 0)
```

## Inverting the color
To invert the color, use the `Color.invert()` method:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
c.invert()
print(c.as_hsv()) # (80, 90, 90)
```

## Applying complemetary harmony rule to the color
To apply the complementaty rule to the current color, use `Color.harmony_complementary()` method:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rule = c.harmony_complementary()
```
This method returns a [HarmonyRule](#harmonyrule-class) object.

## Applying split complemetary harmony rule to the color
To apply the split complementaty rule to the current color, use `Color.harmony_split_complementary()` method. You can also pass an optional argument `phi: int` that indicates the offset in degrees that will be used. By default it is 150deg:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rule = c.harmony_split_complementary(phi=40) # The offset used is 40deg
```

This method returns a [HarmonyRule](#harmonyrule-class) object.

## Applying triadic harmony rule to the color
To apply the triadic rule to the current color, use `Color.harmony_triadic()` method.
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rule = c.harmony_triadic()
```

This method returns a [HarmonyRule](#harmonyrule-class) object.

## Applying tetradic harmony rule to the color
To apply the tetradic rule to the current color, use `Color.harmony_tetradic()` method.
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rule = c.harmony_tetradic()
```

This method returns a [HarmonyRule](#harmonyrule-class) object.

## Applying analogous harmony rule to the color
To apply the split complementaty rule to the current color, use `Color.harmony_analogous()` method. You can also pass an optional argument `phi: int` that indicates the offset in degrees that will be used. By default it is 30deg:
```python
from iris import Color

hue, saturation, value = 260, 90, 90

c = Color.from_hsv(hue, saturation, value)
rule = c.harmony_split_complementary(phi=40) # The offset used is 40deg
```

This method returns a [HarmonyRule](#harmonyrule-class) object.

# HarmonyRule class
This class is a dataclass that is used by Iris to describe any harmony rule that has been applied to the color.

It has 3 attributes:
* `rule_type: str` - This attribute stores the type of rule that was applied. Available types are: `complementary`, `split_complementary`, `triadic`, `tetradic`, `analogous`
* `base_color: Color` - This attribute stores the base color (the color that the rule was applied to)
* `secondary_colors: List[Color]` - This attribute stores a list of colors that were derived from the base one according to the harmony rule

All these attributes have their appropriate getters.

# Method chaining
The Iris' Color class implements method chaining, allowing you to write simple, concise and practical one-liners, such as:

### Simple color conversion
```python
from iris import Color
c = Color.from_hsv(260, 90, 90).as_hex()
v = Color.from_rgb(145, 90, 10).as_cmyk()
# ...
g = Color.from_hex("#ff0097").as_hsv()
```

### Color processing strings
```python
from iris import Color
new_color = Color.from_rgb(old.r, old.g, old.b).invert().lighten(15).hue_shift(10).as_cmyk()
```

