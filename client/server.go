package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"

	echotemplate "github.com/foolin/echo-template"
	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

type AccessToken struct {
	Token        string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
	ExpiresIn    string `json:"expires_in"`
}

type UserInfo struct {
	Campus string `json:"campus"`
	Roles  []struct {
		Type          string `json:"type"`
		Registrations []struct {
			Name          string   `json:"name"`
			Acronym       string   `json:"acronym"`
			ID            string   `json:"id"`
			AcademicTerms []string `json:"academicTerms"`
		} `json:"registrations"`
	} `json:"roles"`
	Photo struct {
		Type string `json:"type"`
		Data string `json:"data"`
	} `json:"photo"`
	Name               string        `json:"name"`
	Gender             string        `json:"gender"`
	Birthday           string        `json:"birthday"`
	Username           string        `json:"username"`
	Email              string        `json:"email"`
	DisplayName        string        `json:"displayName"`
	InstitutionalEmail string        `json:"institutionalEmail"`
	PersonalEmails     []string      `json:"personalEmails"`
	WorkEmails         []interface{} `json:"workEmails"`
	WebAddresses       []interface{} `json:"webAddresses"`
	WorkWebAddresses   []interface{} `json:"workWebAddresses"`
}

var users map[string]UserInfo
var fenixKey = "***REMOVED***"
var fenixID = "***REMOVED***"
var fenixRedirect = "http://127.0.0.1:9090/auth"
var defaultAPIServer = "http://127.0.0.1:5000"

func init() {
	users = make(map[string]UserInfo)
}

func user(c echo.Context) error {
	if _, ok := users[c.Param("id")]; !ok {
		return c.Redirect(http.StatusFound, "/")
	}

	return c.Render(http.StatusOK, "user.html", echo.Map{
		"user":     c.Param("id"),
		"userInfo": users[c.Param("id")],
	})
}

func admin(c echo.Context) error {
	return c.Render(http.StatusOK, "admin.html", echo.Map{
		"title": "Main website",
	})
}

func auth(c echo.Context) error {
	code := c.QueryParam("code")

	requestURL := "https://fenix.tecnico.ulisboa.pt/oauth/access_token"
	requestData := url.Values{
		"client_id":     {fenixID},
		"client_secret": {fenixKey},
		"redirect_uri":  {fenixRedirect},
		"code":          {code},
		"grant_type":    {"authorization_code"},
	}

	resp, err := http.PostForm(requestURL, requestData)
	if err != nil {
		log.Fatalln(err)
	}
	accessToken := AccessToken{}
	json.NewDecoder(resp.Body).Decode(&accessToken)

	requestURLInfo := "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person?access_token="
	resp, err = http.Get(requestURLInfo + accessToken.Token)
	if err != nil {
		log.Fatalln(err)
	}

	userEntry := UserInfo{}
	json.NewDecoder(resp.Body).Decode(&userEntry)

	users[userEntry.Username] = userEntry

	_, err = http.Get(defaultAPIServer + "/user/" + userEntry.Username)
	if err != nil {
		log.Printf("%s", err)
	}

	return c.Redirect(http.StatusFound, "/user/"+userEntry.Username)
}

func login(c echo.Context) error {
	redirectURL := fmt.Sprintf("https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s", fenixID, fenixRedirect)
	return c.Render(http.StatusOK, "login.html", echo.Map{
		"RedirectURL": redirectURL,
	})

}

func main() {
	e := echo.New()
	e.Renderer = echotemplate.Default()

	g := e.Group("/admin")
	g.Use(middleware.BasicAuth(func(username, password string, c echo.Context) (bool, error) {
		if username == "admin" && password == "123" {
			return true, nil
		}
		return false, nil
	}))
	// u := e.Group("/user")
	e.Static("/", "static")
	e.GET("/", login)
	e.GET("/user/:id", user)
	g.GET("/console", admin)
	e.GET("/auth", auth)
	e.Logger.Fatal(e.Start(":9090"))
}
