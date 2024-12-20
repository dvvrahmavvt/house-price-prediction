
package com.dewi.housing.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AuthController {

    @GetMapping("/login")
    public String loginPage() {
        return "login"; 
    }

    @PostMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password, Model model) {
        // Validasi login, misalnya, dengan mengecek username dan password
        if ("user".equals(username) && "password".equals(password)) {
            return "redirect:http://localhost:8501"; 
        }
        model.addAttribute("error", "Invalid username or password");
        return "login"; 
    }
}
