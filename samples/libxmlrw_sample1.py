#Copyright (c) 2026 Benjamin Winter
#This file is part of libxmlrw which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/libxmlrw for full license details.

#DESCRIPTION
#libxmlrw, a pythonic high-level XML parser to read and write XML files and structures.

#imports
import                              libxmlrw

## 
## BASICS, INITIALIZATION
## 

#initialize instance of library:
xml = libxmlrw.xml()

#initialize new XML structure (empty):
my_xml_struct = xml.new_xml_struct()

## 
## XML DECLARATION
## 

#in a standard use case (UTF-8 file format), setting the XML declaration is not required, but here's the process:
my_xml_struct.declaration.version =     "1.0" #XML standard default value
my_xml_struct.declaration.encoding =    "UTF-8" #XML standard default value; MAY be "UTF-8" OR "UTF-16"
my_xml_struct.declaration.standalone =  "yes" #XML standard default value, this is the only value allowed

### 
## XML ROOT ELEMENT
## 

my_xml_struct.rootelement = xml.new_xml_element(name="My_root_element", value="this is the root elements value")
#overwrite name and value:
my_xml_struct.rootelement.name = "My_root_element"
my_xml_struct.rootelement.value = "this is the root element's value"

### 
## XML ATTRIBUTES
## 

#let's add an XML attribute to our XML root element:
my_xml_struct.rootelement.attributes.append( xml.new_xml_attribute(name="attribute_1",value="attribute #1") )
#again, you can omit the [name] and [value] parameters and instead, set the attributes like this:
my_xml_struct.rootelement.attributes[-1].name = "attribute_1"; my_xml_struct.rootelement.attributes[-1].value = "attribute #1"
#add 3 more attributes to our XML root element:
for i in range(2,5): #2, 3, 4
    my_xml_struct.rootelement.attributes.append( xml.new_xml_attribute(name=f"attribute{i}", value=f"attribute{i}") )

## 
## XML ELEMENTS
## 

#let's add the first child element to our root element:
my_xml_struct.rootelement.children.append( xml.new_xml_element(name="child_element_1", value="child element #1") )
#add 2 attributes to child:
for i in range(1, 3): #1, 2
    my_xml_struct.rootelement.children[-1].attributes.append( xml.new_xml_attribute(name=f"attribute{i}", value=f"attribute{i}") )

## 
## CURRENT STATUS
## 

## We now have our XML structure's root "my_xml_struct", which contains the XML declaration (.declaration) and the XML root element (.rootelement), called "My_root_element".
## "My_root_element" has four attributes total and has a child element called "child_element_1", which also contains two attributes.

#Let's add 3 more children to "My_root_element", each child will contain one attribute:
for i in range(2, 5): #2, 3, 4
    #add child
    my_xml_struct.rootelement.children.append( xml.new_xml_element(name=f"child_element{i}", value=f"child element{i}") )
    #add attribute
    my_xml_struct.rootelement.children[-1].attributes.append( xml.new_xml_attribute(name=f"attribute{i}",value=f"attribute{i}") )
    
## 
## XML COMMENTS
## 

#in libxmlrw, XML comments (e.g. <!-- mycomment -->) are defined like any other element, they just have their [is_comment] attribute set [True];
#the comment string is set via the [value] attribute;
#newlines are allowed with newline char \n;
#Let's modify an existing element to an XML comment:
my_xml_struct.rootelement.children[1].is_comment = True
my_xml_struct.rootelement.children[1].value = "my_comment\nline2\nline3" #set comment text (including 2 newlines)
#by the way: if this element, which is now a comment, would have children, these would get included in the comment string

## 
## PROVIDING MULTI-LINE VALUES
## 

#add a child with multi-line value (\n):
my_xml_struct.rootelement.children.append( xml.new_xml_element(name="child_test_1", value="child test\n_1") )
#add 2 attributes with multi-line value (\n):
my_xml_struct.rootelement.children[-1].attributes.append( xml.new_xml_attribute(name="attrib_multiline", value="multi-line attribute\n") )

## 
## WRITING TO FILE
## 

#Let's write our XML structure created above, to a file called "xml_test.xml":
#We'll also optionally catch the ouput in var [write_str], which is a 1:1 copy of the data that gets written to file; newline character is "\n"
write_str = xml.write(xml_structure = my_xml_struct, path = "xml_test.xml")

## 
## READING FROM FILE
## 

#Reading from file (or from a STR passed to the function) is very easy;
#The output you'll get is an xml structure [xml_struct], the very same which we discussed in detail above and passed to the write() function.
read_xml_struct = xml.read(path = "xml_test.xml")

## 
## READING AND ITERATING xml_struct
## 

#Let's print the structure
def print_children(rootelement,prefix="\t\t"):
    for child in rootelement.children:
        print( f"{prefix}found child \n{prefix}\t... name'{child.name}' \n{prefix}\t... value '{child.value}' \n{prefix}\t... attributes " )
        for attrib in child.attributes:
            print( f"{prefix}\t\t... name '{attrib.name}', value '{attrib.value}' " )
        #sub-children
        for subchild in child.children: print_children(subchild,prefix=(prefix+"\t"))
def print_struct(read_xml_struct):
    print( f"XML STRUCT (SIMPLIFIED STDOUT): " )
    #rootelement
    print(f"\t... found rootelement ")
    print( f"\t\t... name '{read_xml_struct.rootelement.name}' \n\t\t... value '{read_xml_struct.rootelement.value}' \n\t\t...attributes ")
    for attrib in read_xml_struct.rootelement.attributes: print( f"\t\t\t... name '{attrib.name}', value '{attrib.value}' ")
    print("\t... children: ")
    #children
    print_children(read_xml_struct.rootelement)
print_struct(read_xml_struct)

##
## UTF-16 file handling
##

#let's write the struct as a UTF-16 file:
xml.write(xml_structure = read_xml_struct, path = "xml_test_utf16.xml", encoding="utf-16")
#let's read it again:
read_xml_struct_fromUTF16 = xml.read(path = "xml_test_utf16.xml")
#and write it again as a UTF-8 file:
xml.write(xml_structure = read_xml_struct_fromUTF16, path = "xml_test_utf8.xml", encoding="utf-8")

## 
## EXCEPTION HANDLING
## 

#libxmlrw raises it's own exception types only.
#See details in the docs at https://github.com/core2000-eU/libxmlrw

#in the example below, we'll make an invalid call which will raise a GeneralException type (libxmlrw.exceptions.GeneralException).
#This exception type wraps the original exception (python default ValueError, in this case) and exports it in the [original] parameter which we can read.

try:
    write_str = xml.write(xml_structure = my_xml_struct, path = "xml_test_exception.xml", encoding="someEncoding")
except libxmlrw.exceptions.GeneralException as e:
    original_exception = e.original
    print(f"test exception handling: libxmlrw raised exception: \n\t... GeneralException: \n\t\t...type {type(e)}, \n\t\t... exception {e} \n\t... original exception: \n\t\t... type {type(original_exception)}, \n\t\t... exception {original_exception}")

#return
