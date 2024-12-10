package com.dewi.housing.controller;

import com.dewi.housing.dto.HousePriceRequest;
import com.dewi.housing.entity.PredictionResult;
import com.dewi.housing.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;


@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")  // Untuk mendukung request dari Streamlit
public class PredictionController {

    @Autowired
    private PredictionService predictionService;

    @PostMapping("/predict")
    public ResponseEntity<?> predictHousePrice(@RequestBody HousePriceRequest request) {
        try {
            double predictedPrice = predictionService.predictAndSavePrice(request);
            
            Map<String, Object> response = new HashMap<>();
            response.put("predictedPrice", predictedPrice);
            
            return ResponseEntity.ok(response);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                .body(Map.of("error", "Terjadi kesalahan dalam prediksi"));
        }
    }
}