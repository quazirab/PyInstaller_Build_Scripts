import os

def specCreator(buildType='debug'):
    '''
    Takes buildType as argument
    '''
    spec = None
    with open(f'build/{buildType}.spec','r') as file:
        spec = file.read()
    current_path = repr(os.getcwd()).replace("'","")
    spec = spec.replace("{current_path}",current_path)

    with open(f'build/r{buildType}.spec','w') as file:
         file.write(spec)

if __name__ == "__main__":
    specCreator()