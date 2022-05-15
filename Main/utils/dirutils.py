#%%
import logging
import os as _os
import re as _re
import h5py as _h5py

def checkdir(dirpath:str):
    dirpath = _os.path.expanduser(dirpath)
    if _os.path.isdir(dirpath) == False:
        checkdir(_os.path.dirname(dirpath))
        _os.mkdir(dirpath)
        print(f"create new dir {dirpath}\n")
        
def files(dir:str) -> list:
    dir = _os.path.expanduser(dir)
    filelist = [ f for f in _os.listdir(dir) if 
    _os.path.isfile(_os.path.join(dir, f))]
    filelist = [x.strip('.pngjpgh5') for x in filelist]
    return filelist

def ls_files(dir):
    """
    return all the filepaths in dir in a string
    """
    filenames = files(dir)
    return '\n'.join(filenames)

def ls_allfiles(dir):
    """
    return all the filepaths including 
    those in subdirs of dir in a string
    """
    filenames = ls_files(dir)
    allfilenames = [ls_files(_os.path.join(dir,f)) 
                    for f in _os.listdir(dir) 
                    if _os.path.isdir(_os.path.join(dir, f))]  
    return filenames+'\n'+'\n'.join(allfilenames)

def ls_light():
    """
    return all the names of LG files below ~/Data/
    """
    base = _os.path.expanduser("~/Data/")
    filelist = files(base)
    r = _re.compile('^LG*')
    lgfilenames =  list(filter(r.match, filelist))
    return base, '\n'.join(lgfilenames)

def ls_BEC():
    """
    return all the names of BEC files below ~/Data/
    """
    base = _os.path.expanduser("~/Data/")
    filelist = files(base)
    r = _re.compile('^BEC\S*')
    lgfilenames =  list(filter(r.match, filelist))
    return base, '\n'.join(lgfilenames)

def ls_data():
    """
    return all the names of data ~/Data/
    """
    base = _os.path.expanduser("~/Data/")
    filelist = files(base)
    r = _re.compile('^scan\S*')
    filenames =  list(filter(r.match, filelist))
    return base, '\n'.join(filenames) + \
           ls_BEC()[1] + ls_light()[1] + \
            ': (Enter to return)\n'
           


def _walk(obj, data, sub):
    for obj_name, obj in obj.items():
        if (isinstance(obj, _h5py.Group)):        
            _walk(obj, data, sub)
        else:
            if obj_name in sub:
                data[sub[obj_name]] = obj[()]
            else:
                data[obj_name] = obj[()]



def retrieve(filename, sub:dict[str, str]={}):
    """ Return the name-var pairs of h5py file.
    Arg:
        filename: h5py file
        sub: dict[varnames in h5 to be substituted, substituting strings] 

    Return: dict[varnames, datasets(in hdf5)]
    """

    path = filename
    datas = {} # read BEC data
    
    with _h5py.File(path, "r") as f:
        _walk(f, datas, sub)
        
        if ('LGfile' in f): # if LG data is stored seperately
            lgpath = _os.path.expanduser(f['LGfile'][()])
            if (lgpath != ''):
                with _h5py.File(lgpath, "r") as f_lg:
                    _walk(f_lg,datas,sub)
                    print(f"\nReading LGdata : {lgpath}\n")
        logging.info("Retrieve data success!\n")
        
    return datas
    


#%%
if __name__ == "__main__":
    # checkdir(r"C:\Users\Lab\Desktop\PlayGround\dir\subdir\subsubdir")
    # print(files(r'c:\\Users\\Lab\\Data'))
    # print(ls_allfiles(r"C:\Users\Lab\Data"))
    # print(ls_light()[1])
    print(ls_data()[1])


# %%
