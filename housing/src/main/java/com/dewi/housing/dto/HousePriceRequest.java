package com.dewi.housing.dto;

public class HousePriceRequest {
    private double price;
    private String address;
    private int bedroomCount;
    private int bathroomCount;
    private int carportCount;
    private double landArea;
    private double buildingArea;
    private int locationEncoded;

    // Getters and Setters
    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
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

    public boolean isValid() {
        
        return price > 0 && address != null && !address.isEmpty();
    }
}