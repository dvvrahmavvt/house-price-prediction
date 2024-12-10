package com.dewi.housing.repository;

import com.dewi.housing.entity.PredictionResult;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PredictionRepository extends JpaRepository<PredictionResult, Long> {
    List<PredictionResult> findByLocationEncoded(int locationEncoded);
}