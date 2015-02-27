# colored
Matplotlib colormaps w/o all of Matplotlib

## Example Usage
```python
>>> import colored as clrd
>>> clrd.cmaps["RdBu"]([0, 0.1, 0.3, 1])
array([[ 0.40392157,  0.        ,  0.12156863],
       [ 0.7008074 ,  0.09965398,  0.17124184],
       [ 0.95455594,  0.64175319,  0.50572859],
       [ 0.01960784,  0.1882353 ,  0.38039216]])
>>> clrd.cmaps["Wistia_r"](0.4)
array([ 1.        ,  0.69568627,  0.        ])
```

## Dependencies
Only `numpy`.
