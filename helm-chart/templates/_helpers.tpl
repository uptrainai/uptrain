{{- define "uptrain.labels" -}}
app.kubernetes.io/name: {{ include "uptrain.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "uptrain.selectorLabels" -}}
app.kubernetes.io/name: {{ include "uptrain.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "uptrain.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "uptrain.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else }}
{{- include "uptrain.name" . }}-{{ .Release.Name }}
{{- end }}
{{- end }}

{{- define "uptrain.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "uptrain.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- "default" }}
{{- end }}
{{- end }}