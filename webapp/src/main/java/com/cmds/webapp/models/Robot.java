package com.cmds.webapp.models;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

/**
 * Class Robot for defining a Robot entity.
 */
@Entity
@Getter
@Setter
@NoArgsConstructor
public class Robot {
    @Id
    public String name;

    public String status;

    @OneToMany
    public List<Delivery> listTrips;

    public Robot(String name, String status, List<Delivery> listTrips){
        this.name = name;
        this.status = status;
        this.listTrips = listTrips;
    }

    public Robot(String name) {
        this.name = name;
        this.status = "";
        this.listTrips = new ArrayList<>();
    }

    public void addTrip (Delivery delivery){
        this.listTrips.add(delivery);

    }

    /**
     * Boolean method for removing a trip from the list of trips.
     * @param tripId A Long trip ID.
     * @return True if the trip was removed, false otherwise.
     */
    public boolean removeTrip (Long tripId) {
        return this.listTrips.removeIf(trip -> trip.getDeliveryId().equals(tripId));
    }

}
