package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func index(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", gin.H{
		"title": "Main website",
	})
}

func main() {
	r := gin.Default()
	r.LoadHTMLGlob("views/*")
	r.Static("/assets", "./node_modules")

	r.GET("/", index)
	r.Run(":9090") // listen and serve on 0.0.0.0:8080
}
