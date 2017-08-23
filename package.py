name = "rezrxt"

authors = [
    "jgerber"
]

version = "0.1.0"
# i probably don't even need this. However, I am going to leave
# this here, as I might want to change to creating a symlink instad
# of calling os.environ
variants = [["python-2.7"]]

description = \
    """
   rezrxt - rez resolve database api & commandline
    """
tools = [
    "rezrxt-add",
    "rezrxt-ls"
]

uuid = "int.rezrxt"

def commands():

    env.PYTHONPATH.append("{root}/python")
    env.ROOT.append("{root}/bin")
   

