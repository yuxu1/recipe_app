from io import BytesIO
import base64
import matplotlib.pyplot as plt


#define get_graph() function to take care of low-level image-handling details
def get_graph():
    #create a BytesIO buffer for the image
    buffer = BytesIO()
    #create a plot with a bytesIO object as a file-like object. set format to png
    plt.savefig(buffer, format='png')
    #set cursor to the beginning of the stream
    buffer.seek(0)
    #retrieve the content of the file
    image_png = buffer.getvalue()
    #encode the bytes-like object
    graph = base64.b64encode(image_png)
    #decode to get the string as output
    graph = graph.decode('utf-8')
    #free up the memory of buffer
    buffer.close()
    #return the image/graph
    return graph


#define function to generate bar chart - recipes by cooking time
def get_bar_chart(data):
    #switch plot backend to AGG(Anti-Grain Geometry)-to write to file
    plt.switch_backend('AGG')
    fig = plt.figure(figsize = (6, 3)) #specify figure size
    plt.bar(data['name'], data['cooking_time'], color='#846EA3')
    plt.xlabel("Recipe Name")
    plt.ylabel("Cooking Time (min)")
    plt.title("Recipes by Cooking Time")
    #plt.xticks(rotation=30, ha='right') #set recipe names at an angle
    plt.gca().spines['right'].set_visible(False) #make right side of frame invisible
    plt.gca().spines['top'].set_visible(False) #make top frame invisible
   
    plt.tight_layout() #specify layout details
    bar_chart = get_graph() #render the graph to file
    return bar_chart

#define function to generate pie chart - number of recipes by difficulty levels
def get_pie_chart(data):
    #switch plot backend to AGG(Anti-Grain Geometry)-to write to file
    plt.switch_backend('AGG')
    fig = plt.figure(figsize = (6,3)) #specify figure size
    #get count of recipes by each difficulty level
    difficulty_counts = data['difficulty'].value_counts()
    labels = difficulty_counts.index #get unique difficulty values
    values = difficulty_counts.values
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#846EA3','#B1A1C9','#99EDBB','#7AA588'])
    plt.title("Recipes by Difficulty Levels")

    plt.tight_layout() #specify layout details
    pie_chart = get_graph() #render the graph to file
    return pie_chart