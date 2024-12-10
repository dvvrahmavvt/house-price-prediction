package com.dewi.housing.controller;

import com.dewi.housing.dto.HousePriceRequest;
import com.dewi.housing.entity.PredictionResult;
import com.dewi.housing.service.PredictionService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class PredictionController {
    private static final Logger logger = LoggerFactory.getLogger(PredictionController.class);

    @Autowired
    private PredictionService predictionService;

    @PostMapping("/predict")
    public ResponseEntity<?> predictHousePrice(@RequestBody HousePriceRequest request) {
        try {
            // Log input request untuk debugging
            logger.info("Received prediction request: {}", request);

            // Prediksi dan simpan harga
            double predictedPrice = predictionService.predictAndSavePrice(request);
            
            // Buat response map dengan detail tambahan
            Map<String, Object> response = new HashMap<>();
            response.put("predictedPrice", predictedPrice);
            response.put("status", "success");
            
            // Log hasil prediksi
            logger.info("Prediction successful. Price: {}", predictedPrice);
            
            return ResponseEntity.ok(response);
        } catch (IllegalArgumentException e) {
            // Log error validasi
            logger.error("Validation error in prediction request", e);
            return ResponseEntity.badRequest().body(Map.of(
                "error", e.getMessage(),
                "status", "error"
            ));
        } catch (Exception e) {
            // Log unexpected error
            logger.error("Unexpected error during prediction", e);
            return ResponseEntity.internalServerError()
                .body(Map.of(
                    "error", "Terjadi kesalahan dalam prediksi: " + e.getMessage(),
                    "status", "error"
                ));
        }
    }

    // Endpoint tambahan untuk melihat prediksi tersimpan (opsional)
    @GetMapping("/predictions")
    public ResponseEntity<?> getAllPredictions() {
        try {
            return ResponseEntity.ok(predictionService.getAllPredictions());
        } catch (Exception e) {
            logger.error("Error retrieving predictions", e);
            return ResponseEntity.internalServerError()
                .body(Map.of(
                    "error", "Gagal mengambil prediksi",
                    "status", "error"
                ));
        }
    }
}