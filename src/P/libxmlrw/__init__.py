#Copyright (c) 2026 Benjamin Winter
#This file is part of libxmlrw which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/libxmlrw for full license details.

#DESCRIPTION
#libxmlrw, a pythonic high-level XML parser to read and write XML files and structures.

#imports
import          os
import          sys
import          copy

#vars, global
read_MaxCharsInstructionsRatio=2 #static: in read(), define how many instructions allowed per char (derived from input) before the function declares an InternalException to prevent endless loops

#classes, global
class templates:
    class xml_struct:
        class element:
            class attribute:
                def __init__(self,name=None,value=None,parent=None):
                    """
                    brief
                    param [name] STR optional, the name
                    param [value] STR optional, the value
                    param [parent] OBJ the parent object
                    returns [] None
                    """
                    self.parent = None if parent is None else parent
                    self.name = "" if name is None else name
                    self.value = "" if value is None else value
            def __init__(self,name=None,value=None,attributes=None,children=None,is_comment=None,parent=None):
                """
                brief
                param [name] STR optional, the name
                param [value] STR optional, the value
                param [attributes] LIST optional, list of templates.xml_struct.element.attribute() -type objects
                param [children] LIST optional, list of templates.xml_struct.element() -type objects
                param [is_comment] BOOL optional, default False
                param [parent] OBJ the parent object
                returns [] None
                """
                self.parent = None if parent is None else parent
                self.name = "" if name is None else name
                self.value = "" if value is None else value
                self.attributes = [] if attributes is None else attributes #attributes, each of type templates.xml_struct.element.attribute()
                self.children = [] if children is None else children #list of sub-elements, each of type templates.xml_struct.element()
                self.is_comment = False if is_comment is None else is_comment #True if element is comment; comment text is stored in value field
                self._is_main_struct = False #internal use only, static, only True for libxmlrw.templates.xml_struct()
                self._closingsyntax_provided = False #internal use only; True when closingsyntax was provided and fully processed
                self._closingsyntax_provided_name = "" #internal use only; stores the name from </name> for checks
        class declaration:
            def __init__(self,version="1.0",encoding="UTF-8",standalone="yes"):
                """
                brief
                param [version] STR optional
                param [encoding] STR optional
                param [standalone] STR optional
                returns [] None
                """
                self.version = version
                self.encoding = encoding
                self.standalone = standalone
                self._already_declared = False #internal use only; to prevent re-declaration
        def __init__(self):
            """
            brief
            returns [] None
            """
            self.declaration = self.declaration()
            self.rootelement = None
            self.children = [] #as comments, even the main structure can have children. list of sub-elements, each of type templates.xml_struct.element()
            self._is_main_struct = True; ##internal use only, static, only True for libxmlrw.templates.xml_struct()
    class s:
        """
        brief INTERNAL: static definitions
        """
        class curract:
            """
            brief INTERNAL: static definitions: currentaction
            """
            for_newlinewhitespace1 = ["comment_started_commentclosing_expected","comment_started_commentclosing_expected__while__element_value_expected","element_attribute_value_expected","element_attribute_quotend_expected"]
            
#custom exceptions
class exceptions:
    """
    brief for details, see the docs
    """
    class XMLRootElementError(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class XMLDeclarationError(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class XMLSyntaxError(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class XMLUnallowedChar(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class XMLMissingName(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class InternalException(Exception):
        def __init__(self,error): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True;
        def __str__(self): return f"{self.error}"
    class GeneralException(Exception):
        def __init__(self,error,original): super().__init__(error); self.error=error; self.is_exception_from_lib_xmlrw=True; self.original=original
        def __str__(self): return f"{self.error}"
    def raiseExceptionToCaller(e):
        """
        internal function to raise exception to the caller correctly
        returns [] None
        """
        if( getattr(e,"is_exception_from_lib_xmlrw",False) ):
            raise e #passthrough self exception types
        else:
            e_repr=str( e.__repr__() )
            raise exceptions.GeneralException(f"{e_repr}",e) from e #wrap other exception types in custom exception
    
#main code
class xml:
    class backend_template:
        def generate_xml_struct(self,xml_structure):
            """
            brief internal function to handle writing xml structure
            param [xml_structure] libxmlrw.templates.xml_struct() the input XML struct
            returns [str_out] STR the output string
            """
            data_out=""
            #checks
            if( not "xml_struct.element" in str(type(xml_structure.rootelement)).lower() ): raise exceptions.XMLSyntaxError(f"generate_xml_struct(): xml structure's [rootelement] attribute MUST be of type [xml_struct.element]")
            if( not "list" in str(type(xml_structure.rootelement.children)).lower() ):      raise exceptions.XMLSyntaxError(f"generate_xml_struct(): xml root element's [children] attribute MUST be of type LIST")
            if( not "list" in str(type(xml_structure.rootelement.attributes)).lower() ):    raise exceptions.XMLSyntaxError(f"generate_xml_struct(): xml root element's [attributes] attribute MUST be of type LIST")
            #handle root element
            data_out+=f"<{xml_structure.rootelement.name}" #<rootelementname
            for attribute in xml_structure.rootelement.attributes:
                data_out+=f" {attribute.name}=\'{attribute.value}\'" # attribute='value'
            data_out+=f">" #>
            if( len(xml_structure.rootelement.children)>0 ):
                #handle root element value
                data_out+=f"\n" #\n
                data_out+=f"\t{xml_structure.rootelement.value}\n" #\trootelementvalue\n
                for child in xml_structure.rootelement.children:
                    #handle children
                    data_out+=self.generate_xml_element(child,f"\t",False)
                #close element
                data_out+=f"</{xml_structure.rootelement.name}>\n" #</elementname>\n
            else:
                #close element
                data_out+=f"{xml_structure.rootelement.value}</{xml_structure.rootelement.name}>\n" #rootelementvalue</rootelementname>\n
            return data_out
        def generate_xml_declaration(self,xml_structure_declaration,declaration_auto_encoding,user_provided_encoding):
            """
            brief internal function to handle writing xml declaration
            param [xml_structure_declaration] ibxmlrw.templates.xml_struct.declaration() the input XML declaration
            param [declaration_auto_encoding] BOOL in [xml_structure] the XML declaration.encoding parameter is automatically adjusted according to the parameter given in [encoding];
                True: auto-generate the [xml_structure] declaration.encoding parameter
                False: do not overwrite the [xml_structure] declaration.encoding parameter;
            param [user_provided_encoding] STR the encoding param the user provided; allowed values: "utf-8" OR "utf-16"; mind capitals;
            returns [str_out] STR the output string
            """
            str_out=""
            #checks
            if( not "xml_struct.declaration" in str(type(xml_structure_declaration)).lower() ): raise exceptions.XMLSyntaxError(f"generate_xml_declaration(): xml structure's [declaration] attribute MUST be of type [xml_struct.declaration]")
            #do
            if( (xml_structure_declaration.version != "") or (xml_structure_declaration.encoding != "") or (xml_structure_declaration.standalone != "") ):
                str_out+=f"<?xml " #<?xml 
                pass;                                               str_out+=f"version=\'{xml_structure_declaration.version}\' "
                if(declaration_auto_encoding):
                    if(user_provided_encoding == "utf-8"):          str_out+=f"encoding=\'UTF-8\' "
                    if(user_provided_encoding == "utf-16"):         str_out+=f"encoding=\'UTF-16\' "
                else:
                    pass;                                           str_out+=f"encoding=\'{xml_structure_declaration.encoding}\' "
                pass;                                               str_out+=f"standalone=\'{xml_structure_declaration.standalone}\' "
                str_out+=f"?>\n" #?>\n
            return str_out
        def generate_xml_element(self,xml_element,prefix,parent_is_comment):
            """
            brief internal function to handle writing xml element including children at a single level
            param [xml_element] libxmlrw.templates.xml_struct.element() the input XML element
            param [prefix) STR the str that is prepended to the output
            param [parent_is_comment] BOOL if set True, [<!-- ] AND [ -->] will not be written even if element is a comment; to prevent nested comments
            returns [str_out] STR the output string
            """
            #prepare
            str_out=""+prefix
            #check xml_element
            if(xml_element._is_main_struct):                                raise exceptions.XMLSyntaxError(f"generate_xml_element(): xml element's [_is_main_struct] attribute cannot be TRUE")
            if( not "list" in str(type(xml_element.children)).lower() ):    raise exceptions.XMLSyntaxError(f"generate_xml_element(): xml element's [children] attribute MUST be of type LIST")
            if( not "list" in str(type(xml_element.attributes)).lower() ):  raise exceptions.XMLSyntaxError(f"generate_xml_element(): xml element's [attributes] attribute MUST be of type LIST")
            #handle element name
            if(xml_element.is_comment==True and parent_is_comment==False):  str_out+=f"<!--"                        #<!--
            else:                                                           str_out+=f"<{xml_element.name}"         #<elementname
            #handle element attributes
            if(not xml_element.is_comment):
                for attribute in xml_element.attributes:            str_out+=f" {attribute.name}=\'{attribute.value}\'" #attribute="value"
                if(True):                                           str_out+=f">" #>
            if( len(xml_element.children)>0 ):
                #handle element value
                if(xml_element.value != ""):
                    if(True):                                       str_out+=f"\n{prefix}\t{xml_element.value}"  #\n\telementvalue
                #handle children
                for child in xml_element.children:
                    if(True):                                       str_out+=f"\n" #\n
                    if(parent_is_comment):                          str_out+=self.generate_xml_element(child,f"{prefix}\t",parent_is_comment)      #handle children
                    else:                                           str_out+=self.generate_xml_element(child,f"{prefix}\t",xml_element.is_comment) #handle children
                #close element
                if(True):                                           str_out+=f"{prefix}"                #
                if(not xml_element.is_comment):                     str_out+=f"</{xml_element.name}>"   #</elementname>
                else:                                               str_out+=f"-->"                     #-->
                if(True):                                           str_out+=f"\n"                      #\n
            #has no children
            else:
                #close element
                if(xml_element.is_comment==True and parent_is_comment==False):  str_out+=f"{xml_element.value}-->\n"                    #elementvalue-->\n
                else:                                                           str_out+=f"{xml_element.value}</{xml_element.name}>\n"  #elementvalue\n\t</elementname>\n
            return str_out
        def write_xml_to_file(self,path,encoding,data):
            """
            brief internal function to handle writing xml structure to file
            param [path] STR filepath
            param [encoding] STR "utf-8"|"utf-16"
            param [data] STR file content
            returns [] None
            """
            with open(path, "w", encoding=encoding) as f: f.write(data)
        def set_element_parents(self,parent,element):
            """
            brief internal function to set the respective parent to [element] and to all of it's attributes and sub-elements (children)
            param [parent] OBJ the parent object for [element] (for it's sub-elements, the parent is determined internally)
            param [element] OBJ the element in question, MUST be an XML element and not an attribute
            returns [] None
            """
            element.parent = parent
            for attr in element.attributes:     attr.parent = element
            for child in (element.children):    self.set_element_parents(element, child)
        def xml_replace_specialchars(self,element):
            """
            brief internal function to replace special chars including to attribues and all child elements
            param [element] OBJ the element in question, MUST be an XML element and not an attribute
            returns [] None
            """
            element.value = element.value.replace("\"","&quot").replace("\'","&quot")
            for attr in element.attributes: attr.value = attr.value.replace("\"","&quot").replace("\'","&quot")
            for child in element.children:  self.xml_replace_specialchars(child)
        def check_element(self,element):
            """
            brief internal function to check elements, attributes for unallowed formats/chars; checks all children of [element] as well
            param [element] OBJ the element in question, MUST be an XML element and not an attribute
            returns [] None
            """
            i=0
            if(element.name == "" and element.is_comment==False):   raise exceptions.XMLMissingName(f"xml element with value \'{element.value}\' is missing name (field name cannot be empty)")
            try:                                                    self.check_xml_name_or_value(name=element.name, value=element.value,exc_on_empty_name=(not element.is_comment))
            except exceptions.XMLUnallowedChar as e:                raise exceptions.XMLUnallowedChar(f"xml element named \'{element.name}\', value \'{element.value}\', contains {e}")
            except exceptions.XMLSyntaxError as e:                  raise exceptions.XMLSyntaxError(f"xml element named \'{element.name}\', value \'{element.value}\' raised XMLSyntaxError '{e}'")
            for attr in element.attributes:
                i+=1
                if(attr.name == "" and attr.parent.is_comment==False):  raise exceptions.XMLMissingName(f"xml element named \'{attr.parent.name}\', with value \'{attr.parent.value}\' contains attribute #[{i}], value \'{attr.value}\', which is missing name (field name cannot be empty)")
                try:                                                    self.check_xml_name_or_value(name=attr.name, value=attr.value,exc_on_empty_name=(not element.is_comment))
                except exceptions.XMLUnallowedChar as e:                raise exceptions.XMLUnallowedChar(f"xml element named \'{element.name}\', value \'{element.value}\', contains attribute #[{i}], which contains {e}")
                except exceptions.XMLSyntaxError as e:                  raise exceptions.XMLSyntaxError(f"xml element named \'{element.name}\', value \'{element.value}\', contains attribute #[{i}] which raised XMLSyntaxError '{e}'")
            for child in element.children: self.check_element(child)
        def split_at_first_of_multiple(self,str_in, split_at):
            """
            brief internal function to split input string at the first occurence of any char(s) in [split_at]. The split only happens ONCE.
            param [str_in] STR the original STR to split
            param [split_at] LIST[STR] LIST of STR characters. multi-chars allowed, e.g. ["--", "##"]
            returns
                [before_split] STR
                [split_char] STR
                [after_split] STR
                [split_char_and_after_split] STR
                e.g. str_in="test_string_with-special-chars", split_at=["_", "-"] -> output: ['test', '_', 'string_with-special-chars', '_string_with-special-chars']
                e.g. str_in="test_string_with-special-chars", split_at=["*", "#"] -> output: ['test_string_with-special-chars', '', '', '']
            """
            curr_index = -1;
            curr_index_position_in_str = -1;
            best_index = -1;
            for split_at_curr in split_at:
                curr_index+=1;
                if(split_at_curr == ""): raise ValueError(f"split_at_first_of_multiple(): param [split_at]: value at index [{curr_index}] cannot be empty")
                if(str_in.find(split_at_curr) > -1):
                    if(best_index == -1):                                                       best_index=curr_index; curr_index_position_in_str=str_in.find(split_at_curr)
                    elif( (best_index > -1) and \
                        (str_in.find(split_at_curr) < curr_index_position_in_str) ):            best_index=curr_index; curr_index_position_in_str=str_in.find(split_at_curr)
                    else:                                                                       pass;
            if(best_index == -1):
                return (  str_in,  "",  "", ""  )
            else:
                out_before_split=str_in.split(split_at[best_index],1)[0]
                out_split_char=split_at[best_index]
                out_after_split=str_in.split(split_at[best_index],1)[1]
                out_split_char_and_after_split=( str(out_split_char)+str(out_after_split) )
                return ( out_before_split,out_split_char,out_after_split,out_split_char_and_after_split )
        def check_xml_name_or_value(self,name=None,value=None,exc_prepend="",exc_append="",exc_on_empty_name=True):
            """
            brief internal function to check XML name or value for unallowed characters. 
            param [name] STR the name to check, leave default if not provided
            param [value] STR the value to check, leave default if not provided
            param [exc_prepend] STR the STR to prepend to the exception text
            param [exc_append] STR the STR to append to the exception text
            param [exc_on_empty_name] BOOL raise exception when name is empty? [True|False]
            returns [] None
            """
            if(name != None):
                if(name=="" and exc_on_empty_name): raise exceptions.XMLSyntaxError(f"{exc_prepend}name cannot be empty{exc_append}")
                _, f_out, _, _ = self.split_at_first_of_multiple( name, ["<",">","&","\"","\'","/>","</"," "] )
                if(f_out != ""): raise exceptions.XMLUnallowedChar(f"{exc_prepend}char(s) \'{f_out}\' not allowed in name \'{name}\'{exc_append}")
            if(value != None):
                _, f_out, _, _ = self.split_at_first_of_multiple( value, ["<",">","\'","/>","</"] )
                if(f_out != ""): raise exceptions.XMLUnallowedChar(f"{exc_prepend}char(s) \'{f_out}\' not allowed in value \'{value}\'{exc_append}")
        def handle_xml_value_newlines(self,element,prefix):
            """
            brief internal function to correctly render newlines in XML values
            returns [] None
            """
            element.value = element.value.replace("\n", ("\n"+prefix+"\t"))
            for attr in element.attributes:
                attr.value = attr.value.replace("\n", ("\n"+prefix+"\t"))
            for child in element.children:
                self.handle_xml_value_newlines(child,(prefix+"\t"))
        def check_encoding_param(self,encoding):
            """
            brief check user-provided [encoding] param
            param [encoding] user-provided encoding param
            returns [] None
            """
            if(encoding!="utf-8" and encoding!="utf-16"): raise ValueError("param [encoding] accepts 'utf-8','utf-16' only, mind capitals")
        def check_file_utf8_or_utf16(self,path):
            """
            brief internal function to check whether an XML file is in UTF-8 encoding or UTF-16 encoding. Only forks for XML usecase because XML requires BOM.
            param [path] STR the file path
            returns [encoding] STR "utf-8"|"utf-16"
            """
            #XML supports UTF-8 and UTF-16 only. That makes it easier for us.
            #XML requires a BOM on bytes 1-2 if UTF-16 is used. This makes it very easy for us.
            with open(path, 'rb') as f:
                bom = f.read(2)
                if bom in (b'\xff\xfe', b'\xfe\xff'):   return("utf-16")
                else:                                   return("utf-8")
        def remove_whites(self,str_in,left=False,right=False,chars_to_remove=[" ","\t"]):
            """
            brief internal function to remote white spaces, tabs, etc. from string (from left and right side)
            param [str_in] STR
            param [left] BOOL remove from left side [True|False]
            param [right] BOOL remove from right side [True|False]
            param [chars_to_remove] LIST the LIST of STR to remove from string
            returns [str_out] STR
            """
            str_out=str_in
            if(left):
                match_found=True
                while(match_found):
                    match_found=False
                    for char_curr in chars_to_remove:
                        if( str_out.startswith(char_curr) ): match_found=True; str_out=str_out[ len(char_curr): ]
            if(right):
                match_found=True
                while(match_found):
                    match_found=False
                    for char_curr in chars_to_remove:
                        if( str_out.endswith(char_curr) ): match_found=True; str_out=str_out[ :len(char_curr)*(-1) ]
            return str_out
        def str_mode_match(self,str_in,str_exp,curract_in,curract_exp,line_num=-1,where="left",exc_prepend="",exc_append="",raise_exc=True):
            """
            brief internal function to match expected string and currentaction, or raise exception
            param [str_in] STR the entire input STR
            param [str_exp] STR the str that is expected and searched for
            param [curract_in] STR the currentaction
            param [curract_exp] STR or LIST: the expected currentaction (you can define multiple in a LIST]
            param [line_num] INT the line number to include when raising exception
            param [where] STR ["left"|"right"] where str_exp is expected, at beginning ("left") or at end ("right")
            param [exc_prepend] STR the STR to prepend to the exception text
            param [exc_append] STR the STR to append to the exception text
            param [raise_exc] BOOL raise exception? True|False; default:True
            returns [decision] BOOL True|False
            """
            #ensure curract_exp is LIST
            if( not "list" in str(type(curract_exp)).lower() ): curract_exp=[curract_exp]
            #do
            for curract_exp_current in curract_exp:
                match where:
                    case "left":
                        if(str_in.startswith(str_exp)) and (curract_exp_current==curract_in):   return True
                    case "right":
                        if(str_in.endswith(str_exp)) and (curract_exp_current==curract_in):     return True
                    case _:                                                                     raise ValueError("str_mode_match(): param [where] accepts 'left','right' only, mind capitals")
            #if we land here, something's not matched up
            if(raise_exc):  raise exceptions.XMLSyntaxError(f"{exc_prepend}XML input line [{line_num}]: unexpected '{str_exp}' to the {where}-most side of string '{str_in}'; (for debugging: currentaction: '{curract_in}'), currentaction epected: '{curract_exp}'{exc_append}")
            else:           pass;
            return False
        def struct_jump_to_root(self,struct_in):
            """
            brief internal function to select root struct from struct_in
            param [struct_in] OBJ
            returns [struct_out] OBJ
            """
            while(struct_in._is_main_struct==False): struct_in=struct_in.parent
            return struct_in
        def struct_check_before_returning(self,struct_in):
            """
            brief internal function to check structure before returning, raises exceptions on errors
            param [struct_in] OBJ struct to check
            returns [] None
            """
            #check self
            if(struct_in._is_main_struct):
                if(struct_in.rootelement._closingsyntax_provided!=True):    raise exceptions.XMLSyntaxError(f"final XML structure check: XML root element named '{struct_in.rootelement.name}', valued '{struct_in.rootelement.value}', is missing closing syntax (for debugging: _closingsyntax_provided is '{struct_in.rootelement._closingsyntax_provided}')")
            else:
                if(struct_in._closingsyntax_provided!=True):                raise exceptions.XMLSyntaxError(f"final XML structure check: XML element named '{struct_in.name}', valued '{struct_in.value}', is missing closing syntax (for debugging: _closingsyntax_provided is '{struct_in._closingsyntax_provided}')")
            #check children
            for child in struct_in.children:
                self.struct_check_before_returning(child)
        def check_chars_instructions_ratio(self,num_chars,num_instructions):
            """
            brief internal function, raises error when [read_MaxCharsInstructionsRatio] exceeded
            param [num_chars] INT
            param [num_instructions] INT
            returns [] None
            """
            if( num_instructions > (num_chars*read_MaxCharsInstructionsRatio) ): raise exceptions.InternalException(f"[read_MaxCharsInstructionsRatio] exceeded, most likely a bug in libxmlrw; please report (for debugging: num_chars is '{num_chars}', num_instructions is '{num_instructions}', read_MaxCharsInstructionsRatio is '{read_MaxCharsInstructionsRatio}')")
        def debug_handle(self,str_in,prepend=f"terminal-only output: libxmlrw: DEBUG: debugging message: ",end=None):
            """
            brief internal function to handle debug messages
            param [self] OBJ
            param [str_in] STR
            param [end] STR passed 1:1 to function print()
            returns [] None
            """
            #stdout
            try:
                if(self.debug and end!=None):   print( f"{prepend}{str_in}",end=end )
                elif(self.debug):               print( f"{prepend}{str_in}" )
            except: pass;
        def __init__(self):
            """
            brief init
            returns [] None
            """
    def new_xml_struct(self):
        """
        brief returns new xml structure
        returns [xml_struct] libxmlrw.templates.xml_struct() -type structure
        """
        try: return copy.copy( templates.xml_struct() )
        except Exception as e: exceptions.raiseExceptionToCaller(e)
    def new_xml_element(self,name=None,value=None,attributes=None,children=None,is_comment=None,parent=None):
        """
        brief returns new xml element
        param [name] STR optional, the name
        param [value] STR optional, the value
        param [attributes] LIST optional, list of templates.xml_struct.element.attribute() -type objects
        param [children] LIST optional, list of templates.xml_struct.element() -type objects
        param [is_comment] BOOL optional, default False
        param [parent] OBJ the parent object
        returns [element] libxmlrw.templates.xml_struct.element() -type structure
        """
        try: return copy.copy( templates.xml_struct.element(name,value,attributes,children,is_comment,parent) )
        except Exception as e: exceptions.raiseExceptionToCaller(e)
    def new_xml_attribute(self,name=None,value=None,parent=None):
        """
        brief returns new xml element
        param [name] STR optional, the name
        param [value] STR optional, the value
        param [parent] OBJ the parent object
        returns [attribute] libxmlrw.templates.xml_struct.element.attribute() -type structure
        """
        try: return copy.copy( templates.xml_struct.element.attribute(name,value,parent) )
        except Exception as e: exceptions.raiseExceptionToCaller(e)
    def read(self,path="",data="",encoding=None):
        """
        brief read an XML structure from a file or directly from input string
        param [path] STR the path of file to read; is neglected if [data] non-empty
        param [data] STR the optional raw data (instead of a file path); takes priority over [path] if both are specified;
            #newlines, if provided, MUST be \n
        param [encoding] STR the encoding for file [path]; allowed values: None OR "utf-8" OR "utf-16"; mind capitals; default:None (auto-detect from file's BOM - set this parameter if auto-detect doesn't suit you);
        returns [xml_structure] the return XML structure
        """
        try:
            #read file or data and load in stack
            if(True):       lines = []
            if(data!=""):   lines=data.split("\n")
            else:
                xml_file_encoding =                                         (self.backend.check_file_utf8_or_utf16(path)) if encoding is None else encoding
                xml.backend_template.debug_handle(self,f"xml file encoding: {xml_file_encoding}")
                with open(path, "r", encoding=xml_file_encoding) as f:      lines=f.readlines()
            #create new xml structure
            currentelement = self.new_xml_struct() #the current element we're working on
            #currentaction is crucial to operation with all possible values:
            currentaction = ""  #""
                                #declaration_opened
                                #element_name_expected
                                #element_attribute_name_expected
                                #element_attribute_eq_expected
                                #element_attribute_quotbegin_expected
                                #element_attribute_value_expected
                                #element_attribute_quotend_expected
                                #element_value_expected
                                #element_closingsyntax_>_expected
                                #comment_started_commentclosing_expected
                                #comment_started_commentclosing_expected__while__element_value_expected
            num_chars=0
            num_instructions=0
            #read
            i = 0 #line count
            for line in lines:
                i+=1
                num_chars+=len(line)
                #handle characters, white-spaces:
                line=line.replace("\"","\'").replace("\r","").replace("\n","")
                line=self.backend.remove_whites( line,left=True )
                thisline_newline_whitespace_added=False
                #
                while(not line==""):
                    xml.backend_template.debug_handle(self,f"we're in line{str(i)}, currentaction:{str(currentaction)}, line:{str(line)}")
                    num_instructions+=1
                    #remove white spaces, tabs
                    if(currentaction=="element_attribute_eq_expected") or \
                        (currentaction=="element_attribute_name_expected") or \
                        (currentaction=="element_attribute_eq_expected") or \
                        (currentaction=="element_attribute_quotbegin_expected") or \
                        (currentaction=="declaration_opened") or \
                        (currentaction==""):                                               line=self.backend.remove_whites( line,left=True )
                    #catch case where line content is zero after while-loop still saw content
                    if(line==""): pass
                    #xml declaration opening
                    elif self.backend.str_mode_match(line,"<?xml",currentaction,"",i,raise_exc=False):
                        line=self.backend.remove_whites( line,right=True )
                        #checks
                        if(i>1): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: XML declaration MUST be the first line in the XML input")
                        if(currentelement._is_main_struct==False): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: XML declaration MUST be the first action in the XML input")
                        if(currentelement.declaration._already_declared): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: re-declaration not allowed")
                        if(currentelement.rootelement!=None): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: root element is already defined, you cannot define XML declaration here")
                        if(not line.endswith("?>")): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: line MUST contain, and end with, '?>'")
                        if(line.count("<") > 1 or line.count(">") > 1): raise exceptions.XMLDeclarationError(f"XML input line [{i}]: XML declaration: contains multiple of chars '<' or '>' which is not allowed")
                        #do
                        line=line[5:] #remove <?xml
                        currentaction="declaration_opened"
                    #xml declaration closing
                    elif self.backend.str_mode_match(line,"?>",currentaction,"declaration_opened",i,raise_exc=False):
                        line=line[2:] #remove ?>
                        currentelement.declaration._already_declared=True
                        currentaction=""
                    #element closingsyntax begin
                    elif self.backend.str_mode_match(line,"</",currentaction,["","element_value_expected"],i,raise_exc=False):
                        line=line[2:] #remove </
                        self.backend.check_xml_name_or_value(name=currentelement.name,value=currentelement.value,exc_prepend=f"XML input line [{i}]: XML element closing syntax '</': ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                        currentaction="element_closingsyntax_>_expected"
                    #comment start
                    elif self.backend.str_mode_match(line,"<!--",currentaction,["","element_value_expected"],i,raise_exc=False):
                        line=line[4:] #remove <!--
                        element_value, _, _, line = self.backend.split_at_first_of_multiple(line,["-->"])
                        if("--" in element_value): raise exceptions.XMLUnallowedChar(f"XML input line [{i}]: XML comment opening syntax '<!--': char(s) '--' not allowed in value '{element_value}' before content '{line}'")
                        xml.backend_template.debug_handle(self,f"elmnt: creating child on currentelement ID {id(currentelement)}, ",end="")
                        currentelement.children.append( self.new_xml_element(value=element_value,is_comment=True,parent=currentelement) )
                        xml.backend_template.debug_handle(self,f"which now has {len(currentelement.children)} children and specifies parent ID {id(currentelement.children[-1].parent)}, and jumping to ",prepend="",end="")
                        currentelement=currentelement.children[-1]
                        xml.backend_template.debug_handle(self,f"{id(currentelement)}; now parent has ID {id(currentelement.parent)}",prepend="")
                        if(currentaction==""):                          currentaction="comment_started_commentclosing_expected"
                        elif(currentaction=="element_value_expected"):  currentaction="comment_started_commentclosing_expected__while__element_value_expected"
                        else: raise exceptions.InternalException(f"XML input line [{i}]: in match-case '<!--': str_mode_match() was called with curract_exp=['','element_value_expected'] but suddenly, currentaction is '{currentaction}' which is unexpected")
                    #comment end
                    elif self.backend.str_mode_match(line,"-->",currentaction,["comment_started_commentclosing_expected","comment_started_commentclosing_expected__while__element_value_expected"],i,raise_exc=False):
                        line=line[3:] #remove -->
                        #final checks
                        if("--" in currentelement.value): raise exceptions.XMLUnallowedChar(f"XML input line [{i}]: XML comment closing syntax '-->': char(s) '--' not allowed in value '{element_value}' before content '{line}'")
                        xml.backend_template.debug_handle(self,f"elmnt: jumping back from {id(currentelement)}, which specifies parent with ID {id(currentelement.parent)} ",end="")
                        xml.backend_template.debug_handle(self,f"and name is '{currentelement.name}' and value is '{currentelement.value}'",prepend="",end="")
                        xml.backend_template.debug_handle(self,f", which specifies parent with ID {id(currentelement.parent)} ",prepend="",end="")
                        currentelement=currentelement.parent #jump to parent
                        xml.backend_template.debug_handle(self,f"to parent with actual ID {id(currentelement)}",prepend="")
                        #currentaction
                        if(currentaction=="comment_started_commentclosing_expected"):                                   currentaction=""
                        elif(currentaction=="comment_started_commentclosing_expected__while__element_value_expected"):  currentaction="element_value_expected"
                        else: raise exceptions.InternalException(f"XML input line [{i}]: in match-case '<!--': str_mode_match() was called with curract_exp=['comment_started_commentclosing_expected','comment_started_commentclosing_expected__while__element_value_expected'] but suddenly, currentaction is '{currentaction}' which is unexpected")
                    #element creation
                    elif self.backend.str_mode_match(line,"<",currentaction,["","element_value_expected"],i,raise_exc=False):
                        line=line[1:] #remove <
                        if(currentelement._is_main_struct) and (currentelement.rootelement!=None):
                            #raise exception on re-definition of XML root element
                            raise exceptions.XMLRootElementError(f"XML input line [{i}]: XML element opening syntax '<': XML root element re-definition not allowed in value '{element_name}' before content '{line}'")
                        elif(currentelement._is_main_struct):
                            xml.backend_template.debug_handle(self,f"elmnt: <: current root structure has ID {id(currentelement)}, currentelement.rootelement is {currentelement.rootelement}, appending new rootelement ",end="")
                            currentelement.rootelement = ( self.new_xml_element(parent=currentelement) )
                            xml.backend_template.debug_handle(self,f"with ID {id(currentelement.rootelement)}, which specifies parent as ID {id(currentelement.rootelement.parent)}, ",prepend="",end="")
                            currentelement=currentelement.rootelement
                            xml.backend_template.debug_handle(self,f"and jumping to rootelement, now with ID {id(currentelement)} and specifying parent ID as {id(currentelement.parent)} ",prepend="")
                        else:
                            xml.backend_template.debug_handle(self,f"elmnt: creating child on currentelement ID {id(currentelement)}, ",end="")
                            currentelement.children.append( self.new_xml_element(parent=currentelement) )
                            xml.backend_template.debug_handle(self,f"which now has {len(currentelement.children)} children and specifies parent ID {id(currentelement.children[-1].parent)}, and jumping to ",prepend="",end="")
                            currentelement=currentelement.children[-1]
                            xml.backend_template.debug_handle(self,f"{id(currentelement)}; now parent has ID {id(currentelement.parent)}",prepend="")
                        currentaction="element_name_expected"
                    #element openingsyntax closing or element closingsyntax closing
                    elif self.backend.str_mode_match(line,">",currentaction,["element_attribute_name_expected","element_closingsyntax_>_expected"],i,raise_exc=False):
                        line=line[1:] #remove >
                        if(currentaction=="element_attribute_name_expected"):
                            self.backend.check_xml_name_or_value(name=currentelement.name,exc_prepend=f"XML input line [{i}]: XML element opening syntax '>': ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                            currentaction="element_value_expected"
                        elif(currentaction=="element_closingsyntax_>_expected"):
                            if(currentelement._closingsyntax_provided_name!=currentelement.name): raise exceptions.XMLSyntaxError(f"line [{i}]: XML element closing syntax '>': closing name '{currentelement._closingsyntax_provided_name}' does not match opening name '{currentelement.name}'")
                            if(currentelement._closingsyntax_provided!=False): raise exceptions.XMLSyntaxError(f"line [{i}]: XML element closing syntax '>': element named '{currentelement.name}' was already closed, unexpected element closing syntax before content '{line}'")
                            currentelement._closingsyntax_provided=True
                            xml.backend_template.debug_handle(self,f"elmnt: jumping back from {id(currentelement)}, which specifies parent with ID {id(currentelement.parent)} ",end="")
                            currentelement=currentelement.parent #jump to parent
                            xml.backend_template.debug_handle(self,f"to parent with actual ID {id(currentelement)}",prepend="")
                            currentaction=""
                        else:
                            raise exceptions.InternalException(f"XML input line [{i}]: in match-case '>': str_mode_match() was called with curract_exp=['element_attribute_name_expected','element_closingsyntax_>_expected'] but suddenly, currentaction is '{currentaction}' which is unexpected")
                    #element self-closing syntax closing
                    elif self.backend.str_mode_match(line,"/>",currentaction,["element_attribute_name_expected"],i,raise_exc=False):
                        line=line[2:] #remove />
                        #checks
                        self.backend.check_xml_name_or_value(name=currentelement.name,exc_prepend=f"XML input line [{i}]: XML element self-closing syntax '/>': ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                        attrib_num=0
                        for attrib in currentelement.attributes:
                            attrib_num+=1
                            self.backend.check_xml_name_or_value(name=attrib.name,value=attrib.value,exc_prepend=f"XML input line [{i}]: XML element self-closing syntax '/>': element contains attribute #{attrib_num}, named '{attrib.name}', ",exc_append=f" of attribute",exc_on_empty_name=False)
                        currentelement._closingsyntax_provided=True
                        xml.backend_template.debug_handle(self,f"elmnt: jumping back from {id(currentelement)}, which specifies parent with ID {id(currentelement.parent)} ",end="")
                        currentelement=currentelement.parent
                        xml.backend_template.debug_handle(self,f"to parent with actual ID {id(currentelement)}",prepend="")
                        currentaction=""
                    #element attribute value opening char =
                    elif self.backend.str_mode_match(line,"=",currentaction,["element_attribute_eq_expected"],i,raise_exc=False):
                        line=line[1:] #remove =
                        currentaction="element_attribute_quotbegin_expected"
                    #element attribute value opening quot '
                    elif self.backend.str_mode_match(line,"'",currentaction,["element_attribute_quotbegin_expected"],i,raise_exc=False):
                        line=line[1:] #remove '
                        currentaction="element_attribute_value_expected"
                    #element attribute value ending quot '
                    elif self.backend.str_mode_match(line,"'",currentaction,["element_attribute_quotend_expected"],i,raise_exc=False):
                        line=line[1:] #remove '
                        #checks
                        attrib_num=len(currentelement.attributes)
                        self.backend.check_xml_name_or_value(name=currentelement.attributes[-1].name,value=currentelement.attributes[-1].value,exc_prepend=f"XML input line [{i}]: XML element attribute definition syntax ''': element contains attribute #{attrib_num}, named '{currentelement.attributes[-1].name}', ",exc_append=f" of attribute",exc_on_empty_name=False)
                        currentaction="element_attribute_name_expected"
                    #assume XML declaration attribute name definition
                    elif self.backend.str_mode_match(line,"",currentaction,["declaration_opened"],i,raise_exc=False):
                        for _ in range( line.count("=") ):
                            #name
                            attrib_name, _, _, line = self.backend.split_at_first_of_multiple(line,["="])
                            attrib_name=self.backend.remove_whites( attrib_name,left=True,right=True )
                            self.backend.check_xml_name_or_value(name=attrib_name,exc_prepend=f"XML input line [{i}]: XML declaration attribute: ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                            line=line[1:] #remove =
                            if( len(line)<1 ):          raise exceptions.XMLSyntaxError(f"line [{i}]: XML declaration: attribute definition: unexpected end-of-line after content '{attrib_name}='")
                            if( line.count("'")<2 ):    raise exceptions.XMLSyntaxError(f"line [{i}]: XML declaration: attribute definition: content that follows '{attrib_name}=' MUST contain at least two ''' chars, before content '{line}'")
                            #value
                            line=self.backend.remove_whites( line,left=True )
                            if(line[0]!="'"): raise exceptions.XMLSyntaxError(f"line [{i}]: XML declaration: attribute definition: after content '{attrib_name}=', expecting char ''', but instead got '{line[0]}' before content '{line}'")
                            line=line[1:] #remove '
                            attrib_value, _, _, line = self.backend.split_at_first_of_multiple(line,["'"])
                            self.backend.check_xml_name_or_value(value=attrib_value,exc_prepend=f"XML input line [{i}]: XML declaration attribute: ",exc_append=f" before content '{line}'")
                            line=line[1:] #remove '
                            if(attrib_name=="version"):         currentelement.declaration.version=attrib_value
                            elif(attrib_name=="encoding"):      currentelement.declaration.encoding=attrib_value
                            elif(attrib_name=="standalone"):    currentelement.declaration.standalone=attrib_value
                            else:                               raise exceptions.XMLDeclarationError(f"line [{i}]: XML declaration: attribute definition: unknown attribute '{attrib_name}' with value '{attrib_value}'")
                    #assume element name
                    elif self.backend.str_mode_match(line,"",currentaction,["element_name_expected"],i,raise_exc=False):
                        element_name, _, _, line = self.backend.split_at_first_of_multiple(line,[" ",">","/>"])
                        self.backend.check_xml_name_or_value(name=element_name,exc_prepend=f"XML input line [{i}]: XML element name definition: ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                        currentelement.name+=element_name
                        currentaction="element_attribute_name_expected"
                    #assume element closingsyntax name
                    elif self.backend.str_mode_match(line,"",currentaction,["element_closingsyntax_>_expected"],i,raise_exc=False):
                        element_name, _, _, line = self.backend.split_at_first_of_multiple(line,[">","/>"])
                        currentelement._closingsyntax_provided_name+=element_name
                    #assume attribute name
                    elif self.backend.str_mode_match(line,"",currentaction,["element_attribute_name_expected"],i,raise_exc=False):
                        attrib_name, _, _, line = self.backend.split_at_first_of_multiple(line,[" ","="])
                        self.backend.check_xml_name_or_value(name=attrib_name,exc_prepend=f"XML input line [{i}]: XML element attribute name definition: ",exc_append=f" before content '{line}'",exc_on_empty_name=True)
                        currentelement.attributes.append( self.new_xml_attribute(name=attrib_name,parent=currentelement) )
                        currentaction="element_attribute_eq_expected"
                    #assume attribute value
                    elif self.backend.str_mode_match(line,"",currentaction,["element_attribute_value_expected","element_attribute_quotend_expected"],i,raise_exc=False):
                        attrib_value, _, _, line = self.backend.split_at_first_of_multiple(line,["'"])
                        self.backend.check_xml_name_or_value(value=attrib_value,exc_prepend=f"XML input line [{i}]: XML element attribute value definition: ",exc_append=f" before content '{line}'")
                        currentelement.attributes[-1].value+=attrib_value
                        currentaction="element_attribute_quotend_expected"
                    #assume element value
                    elif self.backend.str_mode_match(line,"",currentaction,["element_value_expected"],i,raise_exc=False):
                        element_value, _, _, line = self.backend.split_at_first_of_multiple(line,["<"])
                        self.backend.check_xml_name_or_value(value=element_value,exc_prepend=f"XML input line [{i}]: XML element value definition: element with name '{currentelement.name}' defines ",exc_append=f" before content '{line}'")
                        currentelement.value+=element_value
                    #assume comment
                    elif self.backend.str_mode_match(line,"",currentaction,["comment_started_commentclosing_expected","comment_started_commentclosing_expected__while__element_value_expected"],i,raise_exc=False):
                        element_value, _, _, line = self.backend.split_at_first_of_multiple(line,["-->"])
                        if("--" in element_value): raise exceptions.XMLUnallowedChar(f"XML input line [{i}]: XML comment: char(s) '--' not allowed in value '{element_value}' before content '{line}'")
                        currentelement.value+=element_value
                    #default case
                    else: raise exceptions.XMLSyntaxError(f"line [{i}]: unexpected content '{line}' (for debugging: currentaction: '{currentaction}')")
                    #handle newlines
                    if(line==""):
                        if(currentaction in templates.s.curract.for_newlinewhitespace1):
                            if(not thisline_newline_whitespace_added):
                                line+="\n"
                                thisline_newline_whitespace_added=True
                    self.backend.check_chars_instructions_ratio(num_chars,num_instructions)
            #return
            currentelement=self.backend.struct_jump_to_root(currentelement)
            self.backend.struct_check_before_returning(currentelement)
            return currentelement
        except Exception as e: exceptions.raiseExceptionToCaller(e)
    def write(self,xml_structure,path="",encoding="utf-8",declaration_auto_encoding=True,recursionlimit=-1):
        """
        brief write an xml structure (1) to file and/or (2) return as STR to caller
        param [xml_structure] libxmlrw.xml.new_xml_struct() -type structure as input
        param [path] STR optional the path of file to write to
        param [encoding] STR the encoding of file [path]; allowed values: "utf-8" OR "utf-16"; mind capitals; default:"utf-8"
        param [declaration_auto_encoding] BOOL in [xml_structure] the XML declaration.encoding parameter is automatically adjusted according to the parameter given in [encoding];
            True: auto-generate the [xml_structure] declaration.encoding parameter
            False: do not overwrite the [xml_structure] declaration.encoding parameter;
            default:True
        param [recursionlimit] INT raises python's recursion limit if specified;
            If using large XML structures (by default, more than 990 XML elements including all children), make sure to set the [recursionlimit] param.
            This is because the write() function depends on recursion, and it cannot know the size of your structure beforehand.
            Setting the recursionlimit is your responsibility to avoid exceptions.
            [recursionlimit] should match the amount of XML elements + 10, e.g. 9734.
            Not required on smaller structures.
        returns
            [data_out] STR the raw data output; 1:1 copy of the data that gets written to file; newline character is "\n"
        """
        try:
            data_out = ""; #output data
            #handle recursion limit
            recurslimit_before =    sys.getrecursionlimit()
            if(recursionlimit>=0):  sys.setrecursionlimit(recursionlimit)
            #checks
            self.backend.check_encoding_param(encoding)
            if( not "xml_struct" in str(type(xml_structure)).lower() ): raise exceptions.XMLSyntaxError(f"xml structure MUST be of type [xml_struct]")
            if(not xml_structure._is_main_struct == True): raise exceptions.XMLSyntaxError(f"XML structure's attribute [_is_main_struct] MUST be TRUE, not FALSE")
            if(xml_structure.rootelement == None): raise exceptions.XMLSyntaxError(f"XML structure MUST contain root element, currently does not")
            #do mandatory stuff:
            self.backend.set_element_parents(xml_structure, xml_structure.rootelement)
            self.backend.xml_replace_specialchars(xml_structure.rootelement)
            self.backend.check_element(xml_structure.rootelement)
            self.backend.handle_xml_value_newlines(xml_structure.rootelement,"")
            #handle xml declaration
            data_out+=self.backend.generate_xml_declaration(xml_structure.declaration,declaration_auto_encoding,user_provided_encoding=encoding)
            #handle entire xml structure (rootelement+children)
            data_out+=self.backend.generate_xml_struct(xml_structure)
            #handle recursion limit
            if(recursionlimit>=0):  sys.setrecursionlimit(recurslimit_before) #reset to previous value
            #write, return
            self.backend.write_xml_to_file(path,encoding,data_out)
            return str(data_out)
        except Exception as e: exceptions.raiseExceptionToCaller(e)
    def __init__(self,debug=None):
        """
        brief init
        param [debug] BOOL for internal use only; default:False
        returns [] None
        """
        self.backend = self.backend_template()
        self.debug = False if debug is None else debug
