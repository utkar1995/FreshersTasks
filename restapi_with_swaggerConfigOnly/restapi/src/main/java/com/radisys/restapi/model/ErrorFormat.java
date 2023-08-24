package com.radisys.restapi.model;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(accessMode = Schema.AccessMode.READ_ONLY)
public class ErrorFormat {
	private String timestamp;
	private Integer status;
	private String error;
	private String errorMessage;
}
