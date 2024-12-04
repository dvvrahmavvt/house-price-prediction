package com.predict.houseprices.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.predict.houseprices.model.House;

@Repository
public interface HouseRepository extends JpaRepository<House, Long> {}