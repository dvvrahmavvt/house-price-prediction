package com.dewi.housing.service;

import com.dewi.housing.dto.HousePriceRequest;
import com.dewi.housing.entity.PredictionResult;
import com.dewi.housing.repository.PredictionRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.List;


@Service
public class PredictionService {
    private static final Logger logger = LoggerFactory.getLogger(PredictionService.class);

    @Autowired
    private PredictionRepository predictionRepository;

    private final WebClient webClient;

    public PredictionService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
            .baseUrl("http://localhost:5000")
            .build();
    }

    @Transactional
    public double predictAndSavePrice(HousePriceRequest request) {
        // Validasi input
        if (!request.isValid()) {
            throw new IllegalArgumentException("Invalid house price request");
        }

        try {
            // Prediksi harga dari Flask API
            Double predictedPrice = predictPriceFromAPI(request);
            
            // Simpan hasil prediksi
            PredictionResult result = savePredictionResult(request, predictedPrice);
            
            logger.info("Prediction successful: {}", predictedPrice);
            return predictedPrice;
        } catch (Exception e) {
            logger.error("Prediction error", e);
            throw new RuntimeException("Prediksi harga gagal", e);
        }
    }

    private Double predictPriceFromAPI(HousePriceRequest request) {
        return webClient.post()
            .uri("/predict")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(Map.class)
            .map(response -> {
                if (response.containsKey("predictedPrice")) {
                    return ((Number) response.get("predictedPrice")).doubleValue();
                }
                throw new RuntimeException("Invalid API response");
            })
            .block();
    }

    private PredictionResult savePredictionResult(HousePriceRequest request, Double predictedPrice) {
        PredictionResult result = new PredictionResult();
        result.setBedroomCount(request.getBedroomCount());
        result.setBathroomCount(request.getBathroomCount());
        result.setCarportCount(request.getCarportCount());
        result.setLandArea(request.getLandArea());
        result.setBuildingArea(request.getBuildingArea());
        result.setLocationEncoded(request.getLocationEncoded());
        result.setPredictedPrice(predictedPrice);
        result.setPredictionTime(LocalDateTime.now());

        return predictionRepository.save(result);
    }

    // Metode tambahan untuk analisis dan statistik
    public List<PredictionResult> getAllPredictions() {
        return predictionRepository.findAll();
    }

    public List<PredictionResult> getPredictionsByLocation(int locationEncoded) {
        return predictionRepository.findByLocationEncoded(locationEncoded);
    }
}