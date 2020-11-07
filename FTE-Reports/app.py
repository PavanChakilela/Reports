import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

# To Improve speed and cache data
@st.cache(persist=True)
def explore_data(dataset):
    df = pd.read_csv(dataset)
    return df

#PENDING ???
def project_selector(data):
    projectlist = os.listdir(folder_path)
    selected_projectid = st.selectbox('Select a Project', projectlist)
    return selected_projectid
    
#Map Designations 
def map_designations(proj_data):     
    proj_data.loc[proj_data['Grade Id'] == "E80", 'Designation'] = "PAT"
    proj_data.loc[proj_data['Grade Id'] == "E75", 'Designation'] = "PA"
    proj_data.loc[proj_data['Grade Id'] == "E70", 'Designation'] = "PA"   
    proj_data.loc[proj_data['Grade Id'] == "E65", 'Designation'] = "A"
    proj_data.loc[proj_data['Grade Id'] == "E60", 'Designation'] = "SA"
    proj_data.loc[proj_data['Grade Id'] == "E50", 'Designation'] = "M"        
    proj_data.loc[proj_data['Grade Id'] == "E45", 'Designation'] = "SM"
    proj_data.loc[proj_data['Grade Id'] == "E40", 'Designation'] = "AD"
    proj_data.loc[proj_data['Grade Id'] == "E35", 'Designation'] = "D"
    proj_data.loc[proj_data['Grade Id'] == "E33", 'Designation'] = "SD"  
    return proj_data     
    
#Calculate and Display FTE counts 
def display_FTE_count(proj_data):           
    c1,c2,c3, c4 = st.beta_columns([1.2,1,1,1])
            
    with c1:
        with st.beta_expander("Count of Associates"):
            st.write(len(proj_data))

    with c2:
        with st.beta_expander("Total FTE"):
            st.write(proj_data['Allocation Percentage'].sum()/100.0)

    with c3:
        with st.beta_expander("Onsite FTE"):
            on_filter = (proj_data['Offshore/Onsite'] == 'Onsite')
            st.write(proj_data[on_filter]['Allocation Percentage'].sum()/100.0) 

    with c4:
        with st.beta_expander("Offshore FTE"):
            off_filter = (proj_data['Offshore/Onsite'] == 'Offshore')
            st.write(proj_data[off_filter]['Allocation Percentage'].sum()/100.0)
    return proj_data  

#DataFrame for Project FTE split
    #       Offshore    Onsite  TOTAL
    #PAT
    #PA
    #A
    #SA
    #M
    #SM
    #AD
    #D
    #SD
    #TOTAL
def display_FTE_designation_split(proj_data):    
    proj_FTE_matrix = pd.DataFrame({'Offshore' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Onsite' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
                                    'TOTAL' : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})
    
    # round to two decimal places in python pandas 
    pd.set_option('precision', 2)   
    
    proj_FTE_matrix['Designation'] = "PAT PA A SA M SM AD D SD TOTAL".split()
    proj_FTE_matrix.set_index('Designation', inplace=True)
    
    designation_list = ["PAT", "PA", "A", "SA", "M", "SM", "AD", "D", "SD", "TOTAL"]
    location_list = ["Offshore", "Onsite"]
    
    #Per each Designation & Location
    for designation in designation_list:
        for location in location_list:
            des_filter = (proj_data['Designation'] == designation) & (proj_data['Offshore/Onsite'] == location)
            proj_FTE_matrix.loc[designation,location] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0
    
    #Total Offshore
    des_filter = (proj_data['Offshore/Onsite'] == 'Offshore')
    proj_FTE_matrix.loc['TOTAL','Offshore'] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0
        
    #Total Onsite    
    des_filter = (proj_data['Offshore/Onsite'] == 'Onsite')
    proj_FTE_matrix.loc['TOTAL','Onsite'] = proj_data[des_filter]['Allocation Percentage'].sum()/100.0

    #Total Column (sum of Offshore & Onsite rows)
    proj_FTE_matrix.loc[:,'TOTAL'] = proj_FTE_matrix.loc[:,'Offshore'] + proj_FTE_matrix.loc[:,'Onsite']
    
    #Display FTE Designation Matrix View
    cm = sns.light_palette("green", as_cmap=True)
    st.dataframe(proj_FTE_matrix.style.background_gradient(cmap=cm))
    
    return proj_data
    
# MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
def filter_specific_criteria(proj_data, proj2_data):    
    menu_list = st.multiselect("",("Location","Designation","Department","StartDate","EndDate","AssociateName","Supervisor"), key="fil2")
    st.write("You selected",len(menu_list),"fields")
    #print(menu_list, len(menu_list), type(menu_list))
           
    filt_loc = []
    filt_des = []
    filt_dep = []
    filt_name = []
    filt_startdate = []
    filt_enddate = []
    filt_supervisor = []
    for menu_2 in menu_list:
    
        menu_Location = proj2_data['Offshore/Onsite'].unique().tolist()
        menu_Designation = proj2_data['Designation'].unique().tolist()  
        menu_Department = proj2_data['Department Name'].unique().tolist()
        menu_StartDate = proj2_data['Start Date'].unique().tolist()
        menu_EndDate = proj2_data['End Date'].unique().tolist()
        menu_associate_name = proj2_data['Associate Name'].unique().tolist()
        menu_Supervisor = proj2_data['Supervisor Name'].unique().tolist()
        
        if menu_2 == "Location":
            st.subheader("Chose Location")
            filt_loc = st.multiselect("",menu_Location, key="loc")
            
            #Apply Filter
            proj2_filter = (proj2_data['Offshore/Onsite'].isin(filt_loc))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                            
        elif menu_2 == "Designation":
            st.subheader("Chose Designation")
            filt_des = st.multiselect("",menu_Designation, key="des")
            
            #Apply Filter
            proj2_filter = (proj2_data['Designation'].isin(filt_des))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "Department":
            st.subheader("Chose Department")
            filt_dep = st.multiselect("",menu_Department, key="dep")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Department Name'].isin(filt_dep))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
            
        elif menu_2 == "AssociateName":
            st.subheader("Chose AssociateName")
            filt_name = st.multiselect("",menu_associate_name, key="nam")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Associate Name'].isin(filt_name))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "StartDate":
            st.subheader("Chose StartDate")
            filt_startdate = st.multiselect("",menu_StartDate, key="stdate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Start Date'].isin(filt_startdate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "EndDate":
            st.subheader("Chose EndDate")
            filt_enddate = st.multiselect("",menu_EndDate, key="endate")    
            
            #Apply Filter
            proj2_filter = (proj2_data['End Date'].isin(filt_enddate))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]   

        elif menu_2 == "Supervisor":
            st.subheader("Chose Supervisor")
            filt_supervisor = st.multiselect("",menu_Supervisor, key="sup")    
            
            #Apply Filter
            proj2_filter = (proj2_data['Supervisor Name'].isin(filt_supervisor))
            #New filtered PROJ2
            proj2_data = proj2_data[proj2_filter]
                     
    #Display Filtered Dataframe
    st.dataframe(proj2_data[['Associate Id', 'Associate Name', 'Designation', 'Project Name', 'Allocation Percentage', 'Offshore/Onsite', 'Department Name', 'Start Date', 'End Date', 'Supervisor Name']], height=200)
    
    return proj_data, proj2_data
    
def main():

    html_temp = """
		<div style="background-color:{};padding:1px;border-radius:2px">
		<h2 style="color:{};text-align:center;">Project Level Dashboard </h2>
		</div>
		"""
    st.markdown(html_temp.format('royalblue','white'),unsafe_allow_html=True)
    
    menu = ["Project FTE View","RevRec","About"]
    choice = st.sidebar.selectbox("Project FTE View",menu)

    if choice == "Project FTE View":
        

        my_dataset = st.sidebar.file_uploader("Upload IMIS Allocation File in CSV format", type=["csv"])
        if my_dataset is not None:

            #Open IMIS file
            data = explore_data(my_dataset)

            #All Projects, All Associates as-is dataframe
            st.subheader("Show ALL Projects Associates")
                
            with st.beta_expander('Complete View (as-is IMIS report)',expanded=False):
                st.dataframe(data)
                
            #Project Specific
            st.subheader("Show Project specific ASSOCIATE details")
            
            #Remove duplicate project-ids
            project_list = data['Project Id'].unique().tolist()

            #selection based on projects list
            project_id_list = st.multiselect("Pls select project(s)", project_list, key="fil1")
            
            #List of projects for which query is needed
            proj_filt1 = data['Project Id'].isin(project_id_list)
            
            #New dataframe of PROJ selected using multiselect
            proj_data = data[proj_filt1]
            
            #Map Designations   
            proj_data = map_designations(proj_data)        
            
            #Display project specific DataFrame for the selected List of Projects
            st.dataframe(proj_data[['Associate Id', 'Associate Name', 'Designation', 'Project Name', \
            'Allocation Percentage', 'Offshore/Onsite', 'Department Name', 'Start Date', 'End Date', 'Supervisor Name']], height=200)
          
            #Calculate and Display FTE TOTAL counts               
            proj_data = display_FTE_count(proj_data)
            
            #DataFrame for Project FTE split
            proj_data = display_FTE_designation_split(proj_data)
            
            if st.button("Download as file1.csv to Current Folder"):
                proj_data.to_csv("file1.csv")
               
            #MultiSelect based on Location / Designation / Department / StartDate / EndDate / AssociateName / Supervisor
            #New dataframe : PROJ2 before filter same as PROJ
            proj2_data = proj_data
            if st.checkbox("Filter based on Location, Designation, Department, StartDate, EndDate, AssociateName, Supervisor"): 
                proj_data, proj2_data = filter_specific_criteria(proj_data, proj2_data)
                
                proj2_data = display_FTE_designation_split(proj2_data)
                
                if st.button("Download as file2.csv to Current Folder"):
                    proj2_data.to_csv("file2.csv")
        
                  
if __name__ == '__main__':
    main()