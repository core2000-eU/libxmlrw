# 1. libxmlrw
*Well, here's one that will never make it to the standard python library collection... :)*  

*libxmlrw*, a pythonic high-level XML parser to read and write XML files and structures.  
Provides modern, logical XML operations with a focus on real-world use, including intelligent white-space handling and other high-level features.

> [!NOTE]
> This project is in use by **MPSS - Multi-platform shared storage**, a brand-new way to combine, share and access storage over LAN and WAN. Run servers, workstations and clients, multiple OSs and huge numbers of devices simultaneously.  
[Take a look here if that sounds interesting! \[core2000.com\]](https://core2000.com/software/mpss/)  

[Supporters](#now-for-the-boring-part) and contributors are welcome any day of the week :)

## 2. Fast track
Install with `pip install libxmlrw`; import into your project with `import libxmlrw`; and refer to the [documentation](#5-documentation) section below to know your way around; and/or download, open and run example file [`/samples/libxmlrw_sample1.py`](https://github.com/core2000-eU/libxmlrw/blob/main/samples/libxmlrw_sample1.py) from GitHub.  
You can also take a look at the [examples](#55-examples) section below.  

## 3. Basics
**Compatibility**  in short: any platform on Python 3+.  
Here's a list of confirmed options:  

  | Name | Version | Description |
  |------|---------|-------------|
  | -- |
  | Windows 10 |      | ✅ should work   |
  | Windows 11 | 25H2 | ✅ confirmed working  |
  | RHEL/Rocky Linux  | 10        | ✅ confirmed working |
  | -- |
  | Python  | 3.14.2        | ✅ confirmed working |

**Status:** *public beta*.  
The current functions are tested on compatible platforms. There's some features missing here and there (see below) and I'd be glad for feedback on the functions that I plan to never implement (but that might change).  
In short, it will be a while before the release of a final version - but rest assured that current releases are tested extensively and therefore, work within their limitations.

**Built** on W11 25H2 with python 3.14.2, pip 26.2.1, build 1.5.0, twine 7.0.0. Standard settings.

## 4. Installation

  | Type | Details |
  |------|---------|
  | **venv** highly recommended. Please adapt the commands below to your needs. |
  | **Auto install**<br>(preferred, easiest) | run `pip install libxmlrw`, it will download and install from pypi.org |
  | **Manual install from source** | 1. Download the entire source from GitHub<br>2. unpack from ZIP<br>3. run e.g `python -m pip install "/path/to/folder/libxmlrw/" --no-cache-dir` |

## 5. Documentation

### 5.1 Basic usage  
Import with `import libxmlrw`.  
Initialize a new instance with e.g. `xml = libxmlrw.xml()`, where `xml` is now your new instance of the library, on which you call all user-facing functions e.g. `xml.read(*)`, `xml.write(*)`, ... .  

> [!IMPORTANT]
> Please keep the [quirks, features, todo](#56-quirks-features-todo) section in mind below  

> [!IMPORTANT]
> Please, account for this library's special [Exception handling (see below)](#54-exception-handling)  

> [!NOTE]
> For a guide and reference, you may download, open and run example file [`/samples/libxmlrw_sample1.py`](https://github.com/core2000-eU/libxmlrw/blob/main/samples/libxmlrw_sample1.py) from GitHub.  
You can also take a look at the [examples](#55-examples) section below.  

### 5.2 User-facing functions  
- *libxmlrw*. **xml(** *debug=False* **)**  
  **parameters**  
  *(optional) debug* [ *BOOL* ]: set True if you want debugging; dev use only should not be set by the user  
  **returns** \<none\>  
  **raises** \<none\>  
  **description**  
  The main entry function every user MUST call; initializes an instance of this library. E.g. `xml = libxmlrw.xml()`.  

- *userInstance*. **new_xml_struct(** **)**  
  **parameters**  \<none\>  
  **returns**  
  [ *templates.xml_struct()* ]: a new instance of an [*xml_struct*, a structure that represents XML structures programmatically](#53-user-facing-structures).  
  **raises** \<none\>  
  **description**  
  Returns an *xml_struct* for user code.  
  The *new_xml_element(\*)* and *new_xml_attribute(\*)* functions below are sister functions and are also explained [here](#53-user-facing-structures).  

- *userInstance*. **new_xml_element(** *name="",value="",attributes=[],children=[],is_comment=False,parent=None* **)**  
  **parameters**  
  *(optional) name* [ *STR* ]: The XML name of the new element  
  *(optional) value* [ *STR* ]: The XML value of the new element  
  *(optional) attributes* [ *LIST[userInstance. new_xml_attribute(\*)]* ]: The attributes of the new element  
  *(optional) children* [ *LIST[userInstance. new_xml_element(\*)]* ]: The child elements of the new element  
  *(optional) is_comment* [ *BOOL* ]: Set true if this element is an XML comment  
  *(optional) parent* [ *userInstance. new_xml_element(\*)* ]: The parent element  
  **All of the parameters are exported, too and are mutable after instancing: e.g.** `my_new_xml_element.name="xyz"`.  
  **returns**  
  [ *templates.xml_struct.element(*)* ]: a new instance of an XML element for an *xml_struct*  
  **raises** \<none\>  
  **description**  
  Returns a new XML element to be used in an *xml_struct*  

- *userInstance*. **new_xml_attribute(** *name="",value="",parent=None* **)**  
  **parameters**  
  *(optional) name* [ *STR* ]: The XML name of the new attribute  
  *(optional) value* [ *STR* ]: The XML value of the new attribute  
  *(optional) parent* [ *userInstance. new_xml_element(\*)* ]: The parent element  
  **All of the parameters are exported, too and are mutable after instancing: e.g.** `my_new_xml_attrib.name="xyz"`.  
  **returns**  
  [ *templates.xml_struct.element.attribute(*)* ]: a new instance of an XML attribute for an *xml_struct*  
  **raises** \<none\>  
  **description**  
  Returns a new XML attribute to be used in an *xml_struct*  

- *userInstance*. **read(** *path="",data="",encoding=None* **)**  
  **parameters**  
  *(optional) path* [ *STR* ]: the path of file to read; is neglected if *data* non-empty  
  *(optional) data* [ *STR* ]: the optional raw data (instead of a file path); takes priority over *path* if both are specified; newlines, if provided, MUST be \n  
  *(optional) encoding* [ *STR* ]: the encoding for file *path*; allowed values: None OR "utf-8" OR "utf-16"; mind capitals; default:None (auto-detect from file's BOM - set this parameter if auto-detect doesn't suit you)  
  **Either *path* or *data* is required**  
  **returns**  
  [ *templates.xml_struct()* ]: the return XML structure  
  **raises** \<none\>  
  **description**  
  Read an XML structure from a file or directly from input string.  

- *userInstance*. **write(** xml_structure,*path="",encoding="utf-8",recursionlimit=-1* **)**  
  **parameters**  
  xml_structure [ *templates.xml_struct(\*)* ]: User structure as input  
  *(optional) path* [ *STR* ]: optional the path of file to write to  
  *(optional) encoding* [ *STR* ]: the encoding of file *path*; allowed values: "utf-8" OR "utf-16"; mind capitals; default:"utf-8"  
  *(optional) declaration_auto_encoding* [ *BOOL* ]: in [xml_structure] the XML declaration.encoding parameter is automatically adjusted according to the parameter given in [encoding];  
  True: auto-generate the [xml_structure] declaration.encoding parameter  
  False: do not overwrite the [xml_structure] declaration.encoding parameter;  
  default:True  
  *(optional) recursionlimit* [ *INT* ]: raises python's recursion limit if specified;  
  When using large XML structures (by default, more than 990 XML elements including all children), make sure to set the [recursionlimit] param.  
  This is because the write() function depends on recursion, and it cannot know the size of your structure beforehand.  
  Setting the recursionlimit is your responsibility to avoid exceptions.  
  Should match the amount of XML elements + 10, e.g. 9734.  
  Not required on smaller structures.  
  **returns**  
  [ STR ]: the raw data output; 1:1 copy of the data that gets written to file; newline character is "\n"  
  **raises** \<none\>  
  **description**  
  Write an XML structure to file and/or return as STR to caller.  

### 5.3 User-facing structures  
- *libxmlrw*.*templates*. **xml_struct(**  **)**  
  **exports**  
  declaration [ *templates.xml_struct.declaration(\*)* ] the XML declaration  
  rootelement [ *templates.xml_struct.element(\*)* ] the XML root element (the XML rules limit this to max. one)  
  children [ *LIST[templates.xml_struct.element(\*)]* ] the XML child elements (for comments on XMl root element level)  
  **description**  
  To initialize an instance of this structure, please do so by calling *userInstance.new_xml_struct(\*)* only!  
  Represents XML structures programmatically.  
  The user gets such type e.g. from a call to *read(\*)* and *new_xml_struct(\*)* and/or feeds such type e.g. to *write(\*)* functions.  
  This structure stores the XML declaration in the *declaration* export and the XML root element in the *rootelement* export, which may itself store as many children (XML elements, XML attributes) as necessary.  
  This library handles XML comments as "default" XML elements, meaning that all comments are also of type *templates.xml_struct.element(\*)*, but with their *is_comment* export set *TRUE*.  

- *libxmlrw*.*templates*.*xml_struct*. **element(**  **)**  
  **exports**  
  parent [ *templates.xml_struct.element(\*)* ] the parent object; does not have to be filled by user (auto-handled by library)  
  name [ *STR* ] the XML name  
  value [ *STR* ] the XML value  
  attributes [ *LIST[templates.xml_struct.element.attribute(\*)]* ] the XML attributes  
  children [ *LIST[templates.xml_struct.element(\*)]* ] the XML children  
  is_comment [ *BOOL* ] set *TRUE* if this element is XML comment  
  **description**  
  To initialize an instance of this structure, please do so by calling *userInstance.new_xml_element(\*)* only!  
  Represents XML elements programmatically.  
  Each child element is also of this type, making this structure very versatile.  
  The *name*, *value*, *attributes* and *children* exports are self-explainatory;  
  the *is_comment* export is to be set *TRUE* if this element represents an XML comment.  

- *libxmlrw*.*templates*.*xml_struct*.*element*. **attribute(**  **)**  
  **exports**  
  parent [ *templates.xml_struct.element(\*)* ] the parent object; does not have to be filled by user (auto-handled by library)  
  name [ *STR* ] the XML attribute name  
  value [ *STR* ] the XML attribute value  
  **description**  
  To initialize an instance of this structure, please do so by calling *userInstance.new_xml_attribute(\*)* only!  
  Represents XML attributes programmatically.  
  
- *libxmlrw*.*templates*.*xml_struct*. **declaration(**  **)**  
  **exports**  
  version [ *STR* ] the XML declaration version value  
  encoding [ *STR* ] the XML declaration encoding value  
  standalone [ *STR* ] the XML declaration standalone value  
  **description**  
  To initialize an instance of this structure, please use the one provided in function *userInstance.new_xml_struct(\*).declaration* only!  
  Represents XML declarations programmatically.  

### 5.4 Exception handling
**This library itself raises custom exception types only.**    
> [!NOTE]
> Please note the *GeneralException* -type below, which catches all exceptions not listed here (i.e. python built-in exception types), and stores the "original" exception in the *original* export.  

***any user-facing callable of librxmlrw will raise these exception types:***  
- *libxmlrw*.*exceptions*. **XMLRootElementError**  
  **exports** \<none\>  
  **description**  
  Error in XML root element, e.g. duplicate declaration  

- *libxmlrw*.*exceptions*. **XMLDeclarationError**  
  **exports** \<none\>  
  **description**  
  Error in XML declaration, e.g. duplicate declaration or unallowed values  

- *libxmlrw*.*exceptions*. **XMLSyntaxError**  
  **exports** \<none\>  
  **description**  
  Error in XML syntax, e.g. user provided wrong type for *xml_struct*  

- *libxmlrw*.*exceptions*. **XMLUnallowedChar**  
  **exports** \<none\>  
  **description**  
  Unallowed character in name, value or other field  

- *libxmlrw*.*exceptions*. **XMLMissingName**  
  **exports** \<none\>  
  **description**  
  XML name is missing  

- *libxmlrw*.*exceptions*. **InternalException**  
  **exports** \<none\>  
  **description**  
  Library-internal exception which you should most likely report  

- *libxmlrw*.*exceptions*. **GeneralException**  
  **exports**  
  original [ *\** ] the original exception  
  **description**  
  Other exception type (i.e. python built-in exception type) occured which is wrapped in this type; User can access the "original" exception via the *original* export.  

### 5.5 Examples  
> [!NOTE]
> For a vast collection of examples and further reference, open and run example file [`/samples/libxmlrw_sample1.py`](https://github.com/core2000-eU/libxmlrw/blob/main/samples/libxmlrw_sample1.py) from GitHub.

<br>

**Import; initialize instance of library; make new *xml_struct*; define XML declaration**:  
```
import libxmlrw

xml = libxmlrw.xml()
my_xml_struct = xml.new_xml_struct()

#in a standard use case (UTF-8 file format), setting the XML declaration is not required, but here's the process:
my_xml_struct.declaration.version =     "1.0" #XML standard default value
my_xml_struct.declaration.encoding =    "UTF-8" #XML standard default value; MAY be "UTF-8" OR "UTF-16"
my_xml_struct.declaration.standalone =  "yes"
```

**Create XML root element in *xml_struct*; immediately modify (overwrite) name and value**:
```
my_xml_struct.rootelement = xml.new_xml_element(name="My_root_element", value="this is the root elements value")

my_xml_struct.rootelement.name = "My_root_element"
my_xml_struct.rootelement.value = "this is the root element's value"
```

**Add child to XML root element; add attributes to this child**:
```
my_xml_struct.rootelement.children.append( xml.new_xml_element(name="child_element_1", value="child element #1") )

my_xml_struct.rootelement.children[0].attributes.append( xml.new_xml_attribute(name=f"attribute{0}", value=f"attribute{0}") )
my_xml_struct.rootelement.children[0].attributes.append( xml.new_xml_attribute(name=f"attribute{1}", value=f"attribute{1}") )
```

**Add multi-line comment to XML child element; note that comments are handled like "normal" XML elements but with their *is_comment* parameter set true**:
```
my_xml_struct.rootelement.children[0].children.append( xml.new_xml_element(name="comment") )

my_xml_struct.rootelement.children[0].children[0].is_comment = True
my_xml_struct.rootelement.children[0].children[0].value = "my_comment\nline2\nline3"
```

**write *xml-struct* to file on disk**:
```
xml.write(xml_structure = my_xml_struct, path = "xml_test.xml")
```

**read XML file and store as *read_xml_struct***:
```
read_xml_struct = xml.read(path = "xml_test.xml")
```

### 5.6 Quirks, features, ToDo
**Quirks and features**:  
- **This** library handles XML comments as "default" XML elements in *xml_struct*, meaning that all comments are also of type *templates.xml_struct.element(\*)*, but with their *is_comment* export set *TRUE*.  
- **CDATA** is not supported (future release).  
- **namespaces** are not supported (future release).
- **special characters** &, <, >, ", ':  
  - NOT ALLOWED in names (element names, attribute names).  
  - ALLOWED in values ESCAPED-ONLY (element values, attribute values):  
    - escape with:  
      - \& ... &amp  
      - \" ... &quot  
      - \' ... &quot  
      - \< ... &lt  
      - \> ... &gt  
    - the standard specifies that some special chars may be allowed even in values, **this will never be implemented**.  
    - on read() and write(), ALL [\"] are replaced with [\&quot].  
- **Mixed content** is not allowed and will probably never be implemented:  
  - not allowed:  
    \<a> CAT \<b>AND_MOUSE\</b> AND_DOG \</a>  
- **comment within XML element value** are not supported, and will probably never be implemented.  
- **old-school schema** mechanism not supported, only XSD.  
- **multi-line strings**:  
  - for function **read()**:  
    - **multi-line comments** are supported  
    - **multi-line element values** are supported but newline characters get discarded from output - you won't see them  
    - **multi-line attribute values** are supported  
    - **newline character** is '\\n' on output *xml_struct*  
  - for function **write()**:  
    - **newline character** is '\\n'  
    - **multi-line comments** are supported  
    - **multi-line element values** are supported but newline characters get discarded from output  
    - **multi-line attribute values** are supported  
- **nested comments** are not supported.  

**ToDo**:  
- in source code, handle I/O data in chunks because right now, the space used in memory is the same or more as I/O data (file) size  

### 5.7 Source file structure (for contributors and developers):  

```
    <root>
        /samples                      -> sample files
        /src                          -> source code: main folder
            /P                        -> source code: python
                /libxmlrw             
                    /__init__.py      -> main source code file (currently the only file)
        LICENSE                       -> LICENSE
        README.md                     -> README
        setup.py                      -> pip installer setup file
```

### 5.8 Source code structure (for contributors and developers):  
`/src/P/libxmlrw/__init__.py` is the main entry file which contains all classes and functions.  
The universal main entry point is the `__init(*)__` function of class `xml` in the `__init__.py` source code file.  
This is a result from the user importing the library `import libxmlrw` and initializing a new instance e.g. `xml = libxmlrw.xml()`.  

On this instance, the user then calls the relevant functions e.g. `xml.read(*)`, `xml.write(*)`.  

On this instance, the user may also request (depending on his needs) a copy of an `xml_struct` which represents A) either an XML structure generated by user code to be written to file/string or B) an XML structure read from file/string to be represented in user code.  
The user may request such an `xml_struct` by calling the `new_xml_struct(*)` function on his instance, e.g. `my_xml_struct = xml.new_xml_struct()`.  
In the source code, this call then triggers a `return copy.copy( templates.xml_struct() )` which is self-explaining.  
The `new_xml_element(*)` and `new_xml_attribute(*)` are sister functions of `new_xml_struct(*)` and initialize and return a new *XML element* or *XML attribute* respectively in a user-friendly way, e.g. to be used in `my_xml_struct`.  

There's two more first-level classes:  
`templates`, which houses some... templates, would you know it. For backend only.  
`exceptions`, which exposes exception handling both to the user and backend.  

## 6. Official Sources

  | Site | URL |
  |------|---------|
  | **GitHub** | [github.com/core2000-eU/libxmlrw](https://github.com/core2000-eU/libxmlrw) |
  | **pypi.org** | [pypi.org/project/libxmlrw](https://pypi.org/project/libxmlrw) |
  | core2000.com (Website/info only, no release) | [core2000.com/software](https://core2000.com/software/) |

## Now for the boring part
**This library is created and maintained free of cost by a real human being /bla /bla /bla ...** You know the deal by now.  
But seriously, monetary support a serious subject and without some income, I cannot continue to publish and maintain.  

Not that anyone needs my gibberish anyways, but if you find it helpful, **please consider the below. Thanks :)**  
--> [**buymeacoffee.com/core2000**](https://buymeacoffee.com/core2000)

## About
Created on 09.2026 and happily maintained since by **core2000** and it's owner, Benjamin Winter.  
For more details, you can pay us a visit over on [**core2000.com**](https://core2000.com/).
