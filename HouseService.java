package com.predict.houseprices.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.predict.houseprices.model.House;
import com.predict.houseprices.repository.HouseRepository;

@Service
public class HouseService {
    private final HouseRepository houseRepository;

    public HouseService(HouseRepository houseRepository) {
        this.houseRepository = houseRepository;
    }

    public List<House> getAllHouses() {
        return houseRepository.findAll();
    }

    public House saveHouse(House house) {
        return houseRepository.save(house);
    }
}