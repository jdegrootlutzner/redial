
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
# 

library(shiny)

shinyUI(fluidPage(
  
  # Application title
  shinyUI(navbarPage("Redial",
                     
                     tabPanel("About",
                              mainPanel(
                                h3( "Project Description"),
                                "Describe the project here"
                                )
                              ),
                     
                     tabPanel("Prototype",
                              mainPanel(
                                
                                fluidRow(
                                column(6,
                                       # julian
                                       tags$audio(src = "https://storage.googleapis.com/telephone-project/temp-stories/story-012/julian-bbq.wav",
                                                  type = "audio/wav", autoplay = NA, controls = NA),
                                       
                                        # michelle
                                         tags$audio(src = "https://storage.googleapis.com/telephone-project/temp-stories/story-002/evolution-002.wav",
                                                    type = "audio/wav", autoplay = NA, controls = NA),
                                       # satvik
                                         tags$audio(src ="https://storage.googleapis.com/telephone-project/temp-stories/story-002/evolution-003.wav",
                                                    type = "audio/wav", autoplay = NA, controls = NA),
                                       # mehdi
                                       tags$audio(src = "https://storage.googleapis.com/telephone-project/temp-stories/story-012/evolution-002.wav",
                                                  type = "audio/wav", autoplay = NA, controls = NA)
                                  
                                  ),
                                column(6,
                                       
                                         tableOutput('prototypeText')
                                         
                                       
                                       )
                                )

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
                  value = 30)
  ),
    
    #,
    
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
))
