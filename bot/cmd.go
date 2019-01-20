package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

// var ServerURL = "http://127.0.0.1:5000"

var serverURL = "***REMOVED***"

type register struct {
	BotID    string `json:"id"`
	Building string `json:"building_ID"`
}

type botMessage struct {
	// BotID   string `json:"id"`
	Message string `json:"content"`
}

func (r *register) register() error {
	rjson, err := json.Marshal(r)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", serverURL+"/bot/register",
		bytes.NewBuffer(rjson))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	body, err := ioutil.ReadAll(resp.Body)
	log.Println(string(body))
	return nil
}

func (m *botMessage) send(botID string) error {
	mjson, err := json.Marshal(m)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", serverURL+"/bot/"+botID+"/message",
		bytes.NewBuffer(mjson))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	body, err := ioutil.ReadAll(resp.Body)
	log.Println(serverURL + "/bot/" + botID + "message :" + string(body))
	return nil
}

func main() {
	reg := register{BotID: "newBot", Building: "Quimica"}
	err := reg.register()
	if err != nil {
		log.Fatal(err)
	}

	for {
		t := time.Now()
		msg := botMessage{Message: "It is now " + t.String()}
		msg.send(reg.BotID)
		time.Sleep(time.Minute * 1)
	}
}
