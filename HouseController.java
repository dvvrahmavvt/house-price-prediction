package com.predict.houseprices.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.predict.houseprices.model.House;
import com.predict.houseprices.service.HouseService;

@RestController
@RequestMapping("/api/houses")
public class HouseController {
    private final HouseService houseService;

    public HouseController(HouseService houseService) {
        this.houseService = houseService;
    }

    @GetMapping
    public List<House> getAllHouses() {
        return houseService.getAllHouses();
    }

    @PostMapping
    public House saveHouse(@RequestBody House house) {
        return houseService.saveHouse(house);
    }
}
