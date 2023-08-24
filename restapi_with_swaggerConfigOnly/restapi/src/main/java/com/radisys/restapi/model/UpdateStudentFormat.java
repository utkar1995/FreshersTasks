package com.radisys.restapi.model;

import javax.validation.constraints.NotEmpty;

//import javax.validation.constraints.NotEmpty;
//import jakarta.validation.constraints.NotEmpty;
//import jakarta.validation.Valid;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
//import javax.validation.constraints.NotNull;
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(accessMode = Schema.AccessMode.READ_ONLY)
public class UpdateStudentFormat {
	Long rollNo;

	@NotEmpty(message = "Name can't be empty")
	
	String name;

	int rank;

}
