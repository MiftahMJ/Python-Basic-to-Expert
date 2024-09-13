package main

import (
    "fmt"
    "github.com/tebeka/selenium"
)

// Utility function to scroll to an element (if needed)
func scrollToElement(wd selenium.WebDriver, element selenium.WebElement) error {
    _, err := wd.ExecuteScript("arguments[0].scrollIntoView();", []interface{}{element})
    if err != nil {
        return fmt.Errorf("Failed to scroll: %v", err)
    }
    return nil
}
