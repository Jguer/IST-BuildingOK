package main

import (
	"net/http"

	"github.com/foolin/echo-template"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

func index(c echo.Context) error {
	return c.Render(http.StatusOK, "index.html", echo.Map{"title": "Page file title!!"})
}

func main() {
	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Renderer = echotemplate.Default()

	e.GET("/", index)

	e.Logger.Fatal(e.Start(":9090"))
}
