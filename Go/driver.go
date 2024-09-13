package main

import (
    "fmt"
    "github.com/tebeka/selenium"
)

// Initialize the driver (Selenium WebDriver setup)
func initDriver() (selenium.WebDriver, error) {
    caps := selenium.Capabilities{"browserName": "chrome"}
    wd, err := selenium.NewRemote(caps, "")
    if err != nil {
        return nil, fmt.Errorf("Failed to open session: %v", err)
    }
    return wd, nil
}
