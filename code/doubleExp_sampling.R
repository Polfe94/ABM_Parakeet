###########################################################
################ +++ GENERIC FUNCTIONS +++ ################
###########################################################

## WRAPPER FUNCTION TO CHANGE DEFAULT ARGUMENTS
kwargs <- function(f, ...){
     fargs <- formals(f)
     Largs <- list(...)
     
     args <- names(Largs)
     for(arg in args){
          fargs[[arg]] <- Largs[[arg]]
     }
     
     formals(f) <- fargs
     return(f)
}

## CALCULATE PROBABILITY OF EXCEDENCE
pEXC <- function(x){
     y <- sort(x)
     j <- unique(y)
     L <- length(j)
     
     result <- numeric(L)
     for(k in seq_len(L-1)){
          result[k] <- length(which(y > j[k])) / length(y)
     }
     
     data.frame(x = j, y = 1 - result)
}

################################################################
################ +++ DISTRIBUTION FUNCTIONS +++ ################
################################################################

## PDF (DOUBLE EXPONENTIAL WITH A 2D ISOTROPIC NORMALIZATION)
ddoubleexp <- function(r, beta, L1, L2, rmin, rmax){
     d1 = beta * ((1 + L1 * rmin)/ L1 **2) * exp(-L1 * rmin)
     d2 = (1- beta) * ((1 + L2 * rmin) / L2 ** 2) * exp(-L2 * rmin)
     d3 = -beta *((1 + L1 * rmax) / L1 ** 2) * exp(-L1 * rmax)
     d4 = -(1- beta)* ((1+L2 * rmax) / L2 ** 2) * exp(-L2 * rmax)
     
     C = (1 / (2 * pi)) * (1 / (d1 + d2 + d3 + d4))
     
     p = C * (beta * exp(-L1 * r) + (1 - beta)*exp(-L2 * r))
}

rexpDOUBLE2= function(N, beta, t1, t2, a=0, b=100000)
{
        f = function(x, beta, t1, t2, u) {
                temp=beta*(exp(-x/t1))+(1-beta)*(exp(-x/t2))
                temp - u 
        }
        
        v <- numeric(N)
        for(i in seq_len(N)){
                out=uniroot(f, lower=a, upper=b, beta=beta,
                            t1=t1, t2=t2, u=runif(1), tol=1e-10)
                v[i]=out$root  
        }
        v
}

######################################################################
################ +++ REJECTION / ACCEPTION METHOD +++ ################
######################################################################

## REJECTION METHOD
# B= 0.4, lambda1=0.05, lambda2=0.5, a=1, b=1000, 
rjc<-function (n, pdf = ddoubleexp, bounded = TRUE, ...) 
{
     
     # define default values for the pdf
     pdf <- kwargs(pdf, ...)
     
     res <- numeric(0)
     
     if(bounded){
          args <- formals(pdf)
          if('rmin' %in% names(args)){
               a <- args$rmin
          } else {
               a <- args$a
          }
          
          if('rmax' %in% names(args)){
               b <- args$rmax
          } else {
               b <- args$b
          }
          
          # find function maximum
          g = optimize(pdf, interval=c(a,b), maximum = TRUE)$objective
     } else {
          g <- optimize(pdf, interval = c(-Inf, Inf), maximum = TRUE)$objective
     }
     
     #rejection loop
     while(length(res)<n){
          x <- runif(1, a, b)
          y <- runif(1, 0, g)
          fx <- pdf(x)
          if(y < fx){
               res <- c(res, x)
          }
     }
     return(res)
}


#### RESULT ####
# params = {beta = 0.0071277; lambda1 = 0.00050245; lambda2 = 0.00909844; rmin = 1; rmax = 3840}
# print(getwd())
# print(sys.frames())
# print(dirname(sys.frame(1)$ofile))
x <- rjc(n = 10, pdf = ddoubleexp, beta = 0.0071277, L1 = 0.00050245, L2 = 0.00909844, rmin = 1, rmax = 3840)
x

