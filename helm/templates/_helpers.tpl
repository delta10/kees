{{/* vim: set filetype=mustache: */}}

{{- define "kees.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kees.fullname" -}}
{{- if contains .Chart.Name .Release.Name -}}
{{- printf "%s-%s" .Release.Name .component | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s-%s" .Release.Name .Chart.Name .component | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "kees.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "kees.labels" -}}
helm.sh/chart: {{ include "kees.chart" . }}
{{ include "kees.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "kees.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kees.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: {{ .component }}
{{- end -}}
