package com.dewi.housing.dto;

public class HousePriceRequest {

    private int bedroomCount;
    private int bathroomCount;
    private int carportCount;
    private double landArea;
    private double buildingArea;
    private int locationEncoded;

    // Getters and Setters

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

    // Method to validate the request
    public boolean isValid() {
    
        return bedroomCount > 0 && bathroomCount >= 0 && carportCount >= 0 && landArea > 0 && buildingArea > 0;
    }
}