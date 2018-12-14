package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

var fenixKey = "***REMOVED***"
var fenixID = "***REMOVED***"
var fenixRedirect = "http://127.0.0.1:9090/auth"

func index(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", gin.H{
		"title": "Main website",
	})
}

func auth(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", gin.H{
		"title": "Main website",
	})
}

func login(c *gin.Context) {
	redirectURL := fmt.Sprintf("https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s", fenixID, fenixRedirect)
	c.HTML(http.StatusOK, "login.html", gin.H{
		"RedirectURL": redirectURL,
	})

}

func main() {
	//gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	r.LoadHTMLGlob("views/*")

	r.GET("/", login)
	r.GET("/ist", index)
	r.GET("/auth", auth)

	r.Run(":9090") // listen and serve on 0.0.0.0:8080
}
