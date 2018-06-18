
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

# reactiveFileReader()
# transcription_text <- read_csv("~/Desktop/telephone-project/google-voice/transcription-text")
library(shiny)

shinyServer(function(input, output, session) {
  

  fileData <- reactiveFileReader(1000, session, 'transcription-text.csv', read.csv)
  output$prototypeText <- renderTable({
    fileData()
    })
  
  output$distPlot <- renderPlot({
    
    # generate bins based on input$bins from ui.R
    x    <- faithful[, 2]
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    
    # draw the histogram with the specified number of bins
    hist(x, breaks = bins, col = 'darkgray', border = 'white')
    
  })
  
})
