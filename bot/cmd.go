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
var ServerURL = "***REMOVED***"

type Register struct {
	BotID    string `json:"id"`
	Building string `json:"building_ID"`
}

type BotMessage struct {
	// BotID   string `json:"id"`
	Message string `json:"message"`
}

func (r *Register) register() error {
	rjson, err := json.Marshal(r)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", ServerURL+"/bot/register",
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

func (m *BotMessage) send(botID string) error {
	mjson, err := json.Marshal(m)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", ServerURL+"/bot/"+botID+"/message",
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
	log.Println(ServerURL + "/bot/" + botID + "message :" + string(body))
	return nil
}

func main() {
	reg := Register{BotID: "exampleBot", Building: "Central"}
	err := reg.register()
	if err != nil {
		log.Fatal(err)
	}

	for {
		t := time.Now()
		msg := BotMessage{Message: "It is now " + t.String()}
		msg.send(reg.BotID)
		time.Sleep(time.Minute * 1)
	}
}
