
library(plumber)
library(AlgDesign)
library(jsonlite)

library(support.CEs)
library(survival)
library(mded)

library(DT)

#library(mlogit)


set.seed(372)

### Helper functions
'%!in%' <- function(x,y)!('%in%'(x,y))
# Helper function to get card profiles DCE
source("rcode_dce_aizaki_01/get_card_profiles_DCE.R")
source("rcode_dce_aizaki_01/get_CAOne_Analysis_DCE.R")
source("rcode_dce_aizaki_01/get_CAOne_Results_DCE.R")
source("rcode_dce_aizaki_01/get_CAOne_sim_matrix_DCE.R")


get_divisors <- function(x){
  #  Vector of numberes to test against
  y <- seq_len(x)
  #  Modulo division. If remainder is 0 that number is a divisor of x so return it
  y[ x%%y == 0 ]
}

# Helper function to save dataframe as json in PostgreSQL
#source("./save_df2db.R")


#* @apiTitle Choice Analysis
#* @apiDescription Full factorial and DCE designs; Endpoints for working with discrete choice designs with no more then 12 questions


#* @filter cors
function(res) {
  res$setHeader('Access-Control-Allow-Origin', '*') # Or whatever
  plumber::forward()
}


#* Log some information about the incoming request
#* @filter logger
function(req){
  cat(as.character(Sys.time()), "-", 
      req$REQUEST_METHOD, req$PATH_INFO, "-", 
      req$HTTP_USER_AGENT, "@", req$REMOTE_ADDR, "\n")
  
  # Forward the request
  forward()
}



#* @post /create_choice_profiles
factorial_design <- function(req, res){

  raw_df <- tryCatch(jsonlite::fromJSON(req$postBody), 
                    error = function(e) NULL)
  if (is.null(data)) {
    res$status <- 400
    return(list(error = "No data provided"))
  }
  
  attributes <- raw_df[names(raw_df) %in% c("n_alternatives", "var_type") == FALSE]
  
  n_alternatives <- as.numeric(raw_df$n_alternatives)
  var_type <- raw_df$var_type
  data_var_type <- jsonlite::fromJSON(jsonlite::toJSON(var_type))
  attributes_nroflevels <-lengths(attributes)

  categorical_attributes <- data_var_type[which(data_var_type$type=='cat'),]$factor
  if (length(categorical_attributes) == 0) categorical_attributes <- NULL
  #categorical_attributes

  continuous_attributes <- data_var_type[which(data_var_type$type=='con' | data_var_type$type=='price'),]$factor
  if (length(continuous_attributes) == 0) continuous_attributes <- NULL
  #continuous_attributes
  
  # print(categorical_attributes)
  # print(identical(continuous_attributes, NULL))
  # print(identical(categorical_attributes, NULL))
  # print(length(continuous_attributes))
  # print(length(categorical_attributes))
  # print('```````````````')
  # print(typeof(categorical_attributes))
  # print(typeof(continuous_attributes))
  
  ## Params preparation and testing
  
  if (length(attributes) %!in% 2:5 ) stop("Number of attributes should be between 2 and 5!")
  
  if (n_alternatives %!in% 2:4) stop("Number of alternatives should be between 2 and 4!")
  
  if (any(attributes_nroflevels %!in% 2:5)) stop("Number of levels should be between 2 and 5!")
  
  if ( dim(data_var_type)[1] != length(attributes)) stop("Type of variable should be stated for all attributes!")
  
  
  prod_profiles <- prod(attributes_nroflevels)
  full_set_quest <- c(4, 6, 8, 9, 10, 12)
  
  
  if(prod_profiles %in% full_set_quest) {
    
    rd <- rotation.design(
      attribute.names = attributes,
      nalternatives = n_alternatives,
      nblocks = 1,
      randomize = TRUE,   # mix-and-match method 
      seed = 123)
    
    design_matrix <- get_design_matrix(rd, categorical_attributes, continuous_attributes)

    if(n_alternatives==2) {
        
        colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
        colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
        
        card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2)
        
        names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
        names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
        card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, BLOCK_2, QES_2))
        
    }
    
    if(n_alternatives==3) {
        
        colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
        colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
        colnames(rd$alternatives$alt.3) <- paste(colnames(rd$alternatives$alt.3), "3", sep = "_")
        
        card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2, rd$alternatives$alt.3)
        
        names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
        names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
        card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, ALT_3, BLOCK_2, BLOCK_3, QES_2, QES_3))

    }
    
    if(n_alternatives==4) {
        
        colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
        colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
        colnames(rd$alternatives$alt.3) <- paste(colnames(rd$alternatives$alt.3), "3", sep = "_")
        colnames(rd$alternatives$alt.4) <- paste(colnames(rd$alternatives$alt.4), "4", sep = "_")
        
        card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2, rd$alternatives$alt.3, rd$alternatives$alt.4)
        
        names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
        names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
        card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, ALT_3, ALT_4, BLOCK_2, BLOCK_3, BLOCK_4, QES_2, QES_3, QES_4))

    }

    print("Full Factorial...")
        
  } else {
    
    ###########################################################
    ### Creating a DCE design
    ###########################################################
    rd <- rotation.design(
      attribute.names = attributes,
      nalternatives = n_alternatives,
      nblocks = 1,
      randomize = TRUE,   # mix-and-match method 
      seed = 372)
    
    design_matrix <- get_design_matrix(rd, categorical_attributes, continuous_attributes)
    
    startpoint <- dim(rd$alternatives$alt.1)[1]/12
    divisors <- get_divisors(rd$design.information$nquestions)[-1]
    divisors <- divisors[divisors>=startpoint]
    print(divisors)
    
    for (dv in divisors) {
      print(dv)
      rd <- rotation.design(
        attribute.names = attributes,
        nalternatives = n_alternatives,
        nblocks = dv,
        randomize = TRUE,   # mix-and-match method
        seed = 123)
      
      design_matrix <- get_design_matrix(rd, categorical_attributes, continuous_attributes)
      
      qe <- rd$design.information$nquestions

      if (qe <= 12) {
        print(qe)
        # -------------------    subset(mtcars, select=-c(mpg,carb))
        if(n_alternatives==2) {
          
          colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
          colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
          
          card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2)
          
          names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
          names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
          card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, BLOCK_2, QES_2))

        }
        
        if(n_alternatives==3) {
          
          colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
          colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
          colnames(rd$alternatives$alt.3) <- paste(colnames(rd$alternatives$alt.3), "3", sep = "_")
          
          card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2, rd$alternatives$alt.3)
          
          names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
          names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
          card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, ALT_3, BLOCK_2, BLOCK_3, QES_2, QES_3))

        }
        
        if(n_alternatives==4) {
          
          colnames(rd$alternatives$alt.1) <- paste(colnames(rd$alternatives$alt.1), "1", sep = "_")
          colnames(rd$alternatives$alt.2) <- paste(colnames(rd$alternatives$alt.2), "2", sep = "_")
          colnames(rd$alternatives$alt.3) <- paste(colnames(rd$alternatives$alt.3), "3", sep = "_")
          colnames(rd$alternatives$alt.4) <- paste(colnames(rd$alternatives$alt.4), "4", sep = "_")
          
          card_profiles <- cbind.data.frame(rd$alternatives$alt.1, rd$alternatives$alt.2, rd$alternatives$alt.3, rd$alternatives$alt.4)
          
          names(card_profiles)[names(card_profiles) == "BLOCK_1"] <- "BLOCK" ### Keep only one Block variable and Question variable
          names(card_profiles)[names(card_profiles) == "QES_1"] <- "QES"
          card_profiles <- subset(card_profiles, select=-c(ALT_1, ALT_2, ALT_3, ALT_4, BLOCK_2, BLOCK_3, BLOCK_4, QES_2, QES_3, QES_4))

        }
        
        # card_profiles <- rd$alternatives
        break()
      }
      if(dv == tail(divisors,1)) stop("There is a problem regarding the BLOCKS and number of questions!") 
      
    }

  } 
  
  #save_df2db(data_frame=card_profiles) ## Save profiles data frame to DB
  
  card_profiles$ANSW <- c("")
  card_profiles ## Return profiles
  
  design_list <- list(card_profiles, design_matrix)
  names(design_list) <- c("card_profiles", "design_matrix")
  print(design_list)
  
  design_list

}



#* @post /get_caone_responses
factorial_design <- function(req, res){
  
  raw_df <- tryCatch(jsonlite::fromJSON(req$postBody), 
                      error = function(e) NULL)
  
  #raw_df<-req$postBody
  
  if (is.null(data)) {
    res$status <- 400
    return(list(error = "No data provided"))
  }
  
  #print(raw_df)
  
  df_responses <- fromJSON(raw_df$responses)
  df_dm <- raw_df$dm
  
  print(df_responses)
  print(df_dm)
  
  choice_indicators <- as.vector(names(df_responses)[names(df_responses) %!in% c("ID","BLOCK")])

  #print(df_responses)
  #print(df_dm)
  #print(choice_indicators)
  df_responses

  ds <- make.dataset(respondent.dataset = df_responses,
                     design.matrix = df_dm,
                     choice.indicators = choice_indicators)

  ds
  
}  


#* @post /get_caone_results
factorial_design <- function(req, res){
  
  start_time <- Sys.time()
  
  raw_df <- tryCatch(jsonlite::fromJSON(req$postBody), 
                     error = function(e) NULL)
  
  #raw_df<-req$postBody
  
  if (is.null(data)) {
    res$status <- 400
    return(list(error = "No data provided"))
  }
  
  question_id <- raw_df$question_id
  print(question_id)


  caresults <- get_caone_results(question_id=question_id, uid="marius",pwd=pw)
  
  #print(caresults)
  
  end_time <- Sys.time()
  print(end_time - start_time)
  caresults
  
}  
