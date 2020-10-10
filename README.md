# ITLAB: COVID-19 Visualisation Dashboard-v2

## Setup

To start working on this project you will need a clean environment to add and delete your own libraries. The files has a <i>requirements.txt</i> file which will contain all the up-to-date libraries being used. make sure you have python install on your machine before proceeding. <b>This setup procedure should only be used if changes are being made on the a machine outside of any of the ITLab servers.</b> 

1. ### Install virtualenv
    1. pip install virtualenv
    2. virtualenv myenv <i>(myenv is the name I chose, any name can be given for the environment)</i>. myenv must be installed in the root directory of this project.
2. ### Activating virtual environment
    <b>If on a MAC/Linux:</b>

    source myenv/bin/activate 

    <b>If using Windows:</b>

    \myenv\Scripts\activate.bat

    <b>Note:</b> these paths will only work if you and the myenv directory are currently in the root directory. 

3. ### Installing libraries

    pip install requirements.txt

Once you complete these steps your environment will be ready to run the most recent updates made to the dashboard by the ITLab visualization team.

## Running Flask 