package com.dewi.housing.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class PredictionResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int bedroomCount;
    private int bathroomCount;
    private int carportCount;
    private double landArea;
    private double buildingArea;
    private int locationEncoded;
    private double predictedPrice;

    private LocalDateTime predictionTime; // Tambahkan atribut ini

    // Getter dan Setter untuk semua atribut
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public int getBedroomCount() {
        return bedroomCount;
    }

    public void setBedroomCount(int bedroomCount) {
        this.bedroomCount = bedroomCount;
    }

    public int getBathroomCount() {
        return bathroomCount;
    }

    public void setBathroomCount(int bathroomCount) {
        this.bathroomCount = bathroomCount;
    }

    public int getCarportCount() {
        return carportCount;
    }

    public void setCarportCount(int carportCount) {
        this.carportCount = carportCount;
    }

    public double getLandArea() {
        return landArea;
    }

    public void setLandArea(double landArea) {
        this.landArea = landArea;
    }

    public double getBuildingArea() {
        return buildingArea;
    }

    public void setBuildingArea(double buildingArea) {
        this.buildingArea = buildingArea;
    }

    public int getLocationEncoded() {
        return locationEncoded;
    }

    public void setLocationEncoded(int locationEncoded) {
        this.locationEncoded = locationEncoded;
    }

    public double getPredictedPrice() {
        return predictedPrice;
    }

    public void setPredictedPrice(double predictedPrice) {
        this.predictedPrice = predictedPrice;
    }

    public LocalDateTime getPredictionTime() {
        return predictionTime;
    }

    public void setPredictionTime(LocalDateTime predictionTime) {
        this.predictionTime = predictionTime;
    }
}