
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
# 

library(shiny)

shinyUI(fluidPage(
  
  # Application title
  shinyUI(navbarPage("Telephone Project",
                     
                     tabPanel("Introduction",
                              mainPanel(
                                h3( "Project Description"),
                                "Describe the project here"
                                )
                              ),
                     
                     tabPanel("Prototype",
                              mainPanel(
                                tableOutput('prototypeText')
                              )),
                     
                     navbarMenu("More",
                                tabPanel("Sub-Component A"),
                                tabPanel("Sub-Component B"))

  )),
  
  
  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins",
                  "Number of bins:",
                  min = 1,
                  max = 50,
                  value = 30),
      tags$audio(src ="http://telephone-project.storage.googleapis.com/prototype-story/1.wav",
                 type = "audio/wav", autoplay = NA, controls = NA)
  ),
    
    #,
    
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
))
