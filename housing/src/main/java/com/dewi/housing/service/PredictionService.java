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
import org.springframework.web.reactive.function.client.WebClientResponseException;
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
        // Validasi input lebih detail
        if (request == null) {
            logger.error("Prediction request is null");
            throw new IllegalArgumentException("Prediction request cannot be null");
        }

        try {
            // Prediksi harga dari Flask API
            Double predictedPrice = predictPriceFromAPI(request);
            
            // Simpan hasil prediksi
            
            PredictionResult result = savePredictionResult(request, predictedPrice);
            
            logger.info("Prediction successful for request: {}, Predicted Price: {}", request, predictedPrice);
            return predictedPrice;
        } catch (WebClientResponseException e) {
            logger.error("API Response Error: Status {}, Body {}", e.getStatusCode(), e.getResponseBodyAsString());
            throw new RuntimeException("Gagal terhubung dengan Flask API", e);
        } catch (Exception e) {
            logger.error("Prediction process failed", e);
            throw new RuntimeException("Prediksi harga gagal", e);
        }
    }

    private Double predictPriceFromAPI(HousePriceRequest request) {
        return webClient.post()
            .uri("/predict")
            .bodyValue(convertRequestToAPIFormat(request))
            .retrieve()
            .bodyToMono(Map.class)
            .map(response -> {
                // Log raw response untuk debugging
                logger.debug("Raw API Response: {}", response);

                // Fleksibel dalam membaca response
                Object priceValue = response.get("predictedPrice") != null 
                    ? response.get("predictedPrice") 
                    : response.get("predicted_price");

                if (priceValue != null) {
                    return ((Number) priceValue).doubleValue();
                }
                throw new RuntimeException("Tidak dapat menemukan prediksi harga di response API");
            })
            .onErrorResume(e -> {
                logger.error("Error in API prediction", e);
                return Mono.error(new RuntimeException("Gagal melakukan prediksi", e));
            })
            .block();
    }

    // Metode tambahan untuk mengonversi request jika perlu
    private Map<String, Object> convertRequestToAPIFormat(HousePriceRequest request) {
        return Map.of(
            "bedroom_count", request.getBedroomCount(),
            "bathroom_count", request.getBathroomCount(),
            "carport_count", request.getCarportCount(),
            "land_area", request.getLandArea(),
            "building_area", request.getBuildingArea(),
            "location_encoded", request.getLocationEncoded()
        );
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

        // Tambahkan log untuk konfirmasi penyimpanan
        PredictionResult savedResult = predictionRepository.save(result);
        logger.info("Prediction result saved with ID: {}", savedResult.getId());
        return savedResult;
    }

    // Metode tambahan untuk analisis dan statistik
    public List<PredictionResult> getAllPredictions() {
        return predictionRepository.findAll();
    }

    public List<PredictionResult> getPredictionsByLocation(int locationEncoded) {
        return predictionRepository.findByLocationEncoded(locationEncoded);
    }
}